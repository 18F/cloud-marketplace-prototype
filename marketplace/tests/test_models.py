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
    team = TeamFactory.create()

    stats = lt.get_stats_for_team(team)
    assert stats.purchased == 0
    assert stats.used == 0
    assert stats.available == 0

    purchase = PurchaseFactory.create(
        license_type=lt,
        license_count=5,
        team=team,
    )

    stats = lt.get_stats_for_team(team)
    assert stats.purchased == 5
    assert stats.used == 0
    assert stats.available == 5

    user = UserFactory.create()
    user.teams.add(team)
    user.save()

    req = LicenseRequestFactory.create(
        license_type=lt,
        user=user,
        team=team,
        status=models.LicenseRequest.GRANTED,
    )

    stats = lt.get_stats_for_team(team)
    assert stats.purchased == 5
    assert stats.used == 1
    assert stats.available == 4


@pytest.mark.django_db
def test_get_license_stats_for_team_by_product_works():
    lt1 = LicenseTypeFactory.create()
    lt2 = LicenseTypeFactory.create(product=lt1.product)

    p1 = PurchaseFactory.create(license_type=lt1, license_count=5)
    p2 = PurchaseFactory.create(license_type=lt2, team=p1.team,
                                license_count=30)

    stats = lt1.product.get_stats_for_team(p1.team)
    assert stats.purchased == 35
