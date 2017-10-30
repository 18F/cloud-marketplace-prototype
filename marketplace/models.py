from django.db import models
from django.contrib.auth.models import User

from . import products


class LicenseRequest(models.Model):
    """
    Represents a request that a user has made for a product license.
    """

    STATUS_CHOICES = [
        # A user has requested a license for the product. The request
        # now needs to be addressed by an administrator or staff member.
        ('requested', 'Requested'),

        # The user was denied a license for the product,
        # because they do not meet some qualification
        # for having one.
        ('denied', 'Denied'),

        # The user has been wait-listed for a license for
        # the product and will be given one as soon as
        # one is available.
        ('waitlisted', 'Wait-listed'),

        # The user once had a license for the product,
        # but no longer has it.
        ('retired', 'Retired'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.CharField(
        db_index=True,
        choices=products.get_all_choices(),
        max_length=products.MAX_SLUG_LENGTH,
    )

    status = models.CharField(
        db_index=True,
        choices=STATUS_CHOICES,
        max_length=50,
    )
