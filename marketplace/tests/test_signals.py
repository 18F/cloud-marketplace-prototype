import pytest

from . import factories


@pytest.mark.django_db
def test_marketplace_info_is_created_with_user():
    user = factories.UserFactory.create()
    assert user.marketplace
    assert user.marketplace.team is None
