import pytest

from marketplace import models
from .factories import *


def test_team_str():
    team = TeamFactory.build()
    assert team.name == str(team)


def test_product_str():
    trello = TrelloFactory.build()
    assert trello.name == str(trello)


def test_license_type_str():
    trello = TrelloFactory.build()
    lt = LicenseTypeFactory.build(name='Enterprise', product=trello)
    assert str(lt) == 'Trello - Enterprise'


@pytest.mark.django_db
def test_license_type_factory_works():
    lt = LicenseTypeFactory.create()
    assert lt.name
    assert lt.product.name
    assert list(lt.product.license_types.all()) == [lt]


@pytest.mark.django_db
def test_purchase_factory_works():
    purchase = PurchaseFactory.create()


@pytest.mark.django_db
def test_license_request_factory_works():
    req = LicenseRequestFactory.create()


@pytest.mark.django_db
def test_is_approved_for_user_works():
    user = UserFactory.create()
    team = TeamFactory.create()
    product = ProductFactory.create(teams_approved_for=[team])
    assert product.is_approved_for_user(user) is False

    team.users.add(user)
    team.save()
    assert product.is_approved_for_user(user) is True


@pytest.mark.django_db
def test_get_availability_for_team_works():
    lt = LicenseTypeFactory.create()
    purchase = PurchaseFactory.create(
        license_type=lt,
        license_count=5,
    )

    assert lt.get_availability_for_team(purchase.team) == 5

    user = UserFactory.create()
    user.teams.add(purchase.team)
    user.save()

    req = LicenseRequestFactory.create(
        license_type=lt,
        user=user,
        team=purchase.team,
        status=models.LicenseRequest.GRANTED,
    )

    assert lt.get_availability_for_team(purchase.team) == 4
