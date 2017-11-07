import pytest

from . import factories


@pytest.mark.django_db
def test_homepage_contains_products(client):
    factories.TrelloFactory.create()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Trello' in response.content


@pytest.mark.django_db
def test_product_pages_exist(client):
    factories.TrelloFactory.create()
    response = client.get('/products/trello/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_nonexistent_product_pages_return_404(client):
    response = client.get('/products/zzz/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_logged_in_users_see_their_email_address(client):
    user = factories.UserFactory.create(email='foo.bar@gsa.gov')
    client.force_login(user)
    response = client.get('/')
    assert b'foo.bar@gsa.gov' in response.content


@pytest.mark.django_db
def test_logout_works(client):
    user = factories.UserFactory.create(email='foo.bar@gsa.gov')
    client.force_login(user)
    response = client.get('/logout')
    assert response.status_code == 200
    assert b'foo.bar@gsa.gov' not in response.content


@pytest.mark.django_db
def test_usage_works(client):
    team = factories.TeamFactory.create(name="Awesome Team")
    product = factories.TrelloFactory.create(teams_approved_for=[team])
    lt = factories.LicenseTypeFactory.create(product=product)

    response = client.get('/usage')
    html = response.content.decode('utf-8')

    assert response.status_code == 200
    assert 'Trello' in html
    assert 'Awesome Team' in html
