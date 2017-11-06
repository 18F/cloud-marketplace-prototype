import pytest
from django.core.exceptions import ValidationError

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


def test_granted_license_requests_must_have_team_set():
    req = LicenseRequestFactory.build()
    req.clean()
    req.status = req.GRANTED
    with pytest.raises(ValidationError,
                       match=r'Granted licenses must have a team set'):
        req.clean()


@pytest.mark.django_db
def test_get_license_stats_for_team_works():
    lt = LicenseTypeFactory.create()
    purchase = PurchaseFactory.create(
        license_type=lt,
        license_count=5,
    )

    stats = lt.get_stats_for_team(purchase.team)
    assert stats.purchased == 5
    assert stats.used == 0
    assert stats.available == 5

    user = UserFactory.create()
    user.teams.add(purchase.team)
    user.save()

    req = LicenseRequestFactory.create(
        license_type=lt,
        user=user,
        team=purchase.team,
        status=models.LicenseRequest.GRANTED,
    )

    stats = lt.get_stats_for_team(purchase.team)
    assert stats.purchased == 5
    assert stats.used == 1
    assert stats.available == 4
