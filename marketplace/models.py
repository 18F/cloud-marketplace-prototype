from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


class Team(models.Model):
    """
    Represents a team of people. This is a fairly abstract
    concept and can represent anything from an entire
    government agency to a small team within an agency.
    """

    name = models.CharField(max_length=100)

    users = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return self.name


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
        user_teams = user.teams.all()
        my_teams = self.teams_approved_for.all()
        return my_teams.intersection(user_teams).exists()

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


class LicenseType(models.Model):
    """
    Represents a type of license for a product, e.g.
    "Free", "Enterprise", "Pro", etc.
    """

    name = models.CharField(
        max_length=50,
    )

    product = models.ForeignKey(
        Product,
        related_name='license_types',
        on_delete=models.CASCADE
    )

    def get_availability_for_team(self, team):
        # Urg, beware of double-counting: e.g. if a user is a
        # member of teams A and B, and A has one free license
        # and B has one free license, which pool does the
        # user draw from?
        #
        # One possibility is to add a 'team' field to the
        # LicenseRequest class, which specifies the pool to
        # draw from.
        raise NotImplementedError('TODO: Finish this!')

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

    teams = models.ManyToManyField(Team)


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
