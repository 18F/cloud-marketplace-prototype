from collections import namedtuple
from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError


class Team(models.Model):
    """
    Represents a team of people. This is a fairly abstract
    concept and can represent anything from an entire
    government agency to a small team within an agency.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserMarketplaceInfo(models.Model):
    """
    This model stores all marketplace-related information
    for a particular user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='marketplace')

    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE,
                             related_name='users')


class Product(models.Model):
    """
    Represents a software product in the marketplace.
    """

    name = models.CharField(max_length=100)

    slug = models.SlugField(max_length=100)

    category = models.CharField(max_length=100)

    description = models.TextField()

    teams_approved_for = models.ManyToManyField(Team)

    def is_approved_for_user(self, user):
        if user.marketplace.team is None:
            return False
        return self.teams_approved_for.filter(
            pk=user.marketplace.team.pk
        ).exists()

    def get_stats_for_team(self, team):
        stats = LicenseStats(0, 0, 0)
        for license_type in self.license_types.all():
            lt_stats = license_type.get_stats_for_team(team)
            stats = LicenseStats(*[
                sum(x) for x in zip(stats, lt_stats)
            ])
        return stats

    @property
    def icon(self):
        return staticfiles_storage.url(
            f"marketplace/products/{self.slug}/icon.png")

    @property
    def primary_screenshot(self):
        return staticfiles_storage.url(
            f"marketplace/products/{self.slug}/primary_screenshot.png")

    @property
    def detail_url(self):
        return reverse('product_detail', kwargs={'product': self})

    def __str__(self):
        return self.name


LicenseStats = namedtuple('LicenseStats', [
    'purchased',
    'used',
    'available',
])


class LicenseType(models.Model):
    """
    Represents a type of license for a product, e.g.
    "Free", "Enterprise", "Pro", etc.
    """

    name = models.CharField(
        max_length=100,
    )

    product = models.ForeignKey(
        Product,
        related_name='license_types',
        on_delete=models.CASCADE
    )

    def get_stats_for_team(self, team):
        now = timezone.now()
        purchased = Purchase.objects.filter(
            license_type=self,
            team=team,
            start_date__lte=now,
            end_date__gt=now,
        ).aggregate(models.Sum('license_count'))['license_count__sum'] or 0
        used = LicenseRequest.objects.filter(
            license_type=self,
            user__marketplace__team=team,
            status=LicenseRequest.GRANTED,
        ).count()
        return LicenseStats(purchased, used, purchased - used)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class Purchase(models.Model):
    """
    Represents a purchase of licenses that have been made for a
    product.
    """

    # Open questions:
    #
    # * What happens when a purchase event's end date is reached?
    #   how do we decide what users lose their licenses, if any?
    #   Or do we simply email an administrator and tell them that
    #   they need to relinquish the licenses for a certain number
    #   of users?

    license_type = models.ForeignKey(LicenseType, on_delete=models.CASCADE)

    license_count = models.IntegerField()

    start_date = models.DateField()

    end_date = models.DateField()

    team = models.ForeignKey(Team, related_name='purchases',
                             on_delete=models.CASCADE)


class LicenseRequest(models.Model):
    """
    Represents a request that a user has made for a product license.
    """

    REQUESTED = 'requested'
    GRANTED = 'granted'
    DENIED = 'denied'
    WAITLISTED = 'waitlisted'
    RELINQUISHED = 'relinquished'

    STATUS_CHOICES = [
        # A user has requested a license for the product. The request
        # now needs to be addressed by an administrator or staff member.
        (REQUESTED, 'Requested'),

        # The user was granted a license for the product.
        (GRANTED, 'Granted'),

        # The user was denied a license for the product,
        # because they do not meet some qualification
        # for having one.
        (DENIED, 'Denied'),

        # The user has been wait-listed for a license for
        # the product and will be given one as soon as
        # one is available.
        (WAITLISTED, 'Wait-listed'),

        # The user once had a license for the product,
        # but no longer has it.
        (RELINQUISHED, 'Relinquished'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    license_type = models.ForeignKey(LicenseType, on_delete=models.CASCADE)

    status = models.CharField(
        db_index=True,
        choices=STATUS_CHOICES,
        max_length=50,
    )

    is_self_reported = models.BooleanField(
        default=False,
        help_text=("The user has self-reported that they have "
                   "a license for this product."),
    )

    def clean(self):
        if self.status == self.GRANTED and self.user.marketplace.team is None:
            raise ValidationError('Users of granted licenses must have a '
                                  'team.')
