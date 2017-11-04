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
def test_license_type_factory_works():
    lt = LicenseTypeFactory.build()
    assert lt.name
    assert lt.product.name
