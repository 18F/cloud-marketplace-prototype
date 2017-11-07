import re
from io import StringIO
import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_seeddb_works():
    out = StringIO()
    call_command('seeddb', stdout=out)
    output = out.getvalue()
    assert 'Created Favro.' in output
    assert 'object at 0x' not in output
    assert 'Created license type' in output
    assert 'Created team' in output
    assert 'Created a purchase of' in output
    assert re.search(r'Added ".*" to team ".*"', output)
    assert 'Created a license request' in output
    assert 'with status "granted"' in output
    assert 'with status "waitlisted"' in output
    assert 'Creating superuser' in output

    out = StringIO()
    call_command('seeddb', stdout=out)
    output = out.getvalue()
    assert 'Favro already exists.' in output
    assert 'Ensuring admin@gsa.gov is a superuser' in output
