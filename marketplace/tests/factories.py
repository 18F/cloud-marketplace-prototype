import factory
from factory.django import DjangoModelFactory as Factory
from django.contrib.auth.models import User

from marketplace import models


class UserFactory(Factory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')

    last_name = factory.Faker('last_name')

    email = factory.LazyAttribute(
        lambda a: f"{a.first_name.lower()}.{a.last_name.lower()}@gsa.gov"
    )

    username = factory.LazyAttribute(
        lambda a: a.email
    )

    is_active = True


def simple_job():
    job = factory.Faker('job').generate({})
    # Some jobs are like "Nurse, adult"; we don't want the part
    # after the comma.
    return job.split(',')[0]


class TeamFactory(Factory):
    class Meta:
        model = models.Team

    name = factory.LazyAttribute(
        lambda a: f"GSA {simple_job()}s"
    )
