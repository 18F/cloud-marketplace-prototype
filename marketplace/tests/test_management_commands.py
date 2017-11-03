from io import StringIO
import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_create_initial_products_works():
    out = StringIO()
    call_command('create_initial_products', stdout=out)
    assert 'Created Favro.' in out.getvalue()

    out = StringIO()
    call_command('create_initial_products', stdout=out)
    assert 'Favro already exists.' in out.getvalue()
