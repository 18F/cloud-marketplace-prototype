import pytest

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


# TODO: We can probably delete this test eventually, right now
# I just want to make sure the factory I've added actually works.
@pytest.mark.django_db
def test_license_type_factory_works():
    lt = LicenseTypeFactory.create()
    assert lt.name
    assert lt.product.name
    assert list(lt.product.license_types.all()) == [lt]


@pytest.mark.django_db
def test_is_approved_for_user_works():
    user = UserFactory.create()
    team = TeamFactory.create()
    product = ProductFactory.create(teams_approved_for=[team])
    assert product.is_approved_for_user(user) is False

    team.users.add(user)
    team.save()
    assert product.is_approved_for_user(user) is True
