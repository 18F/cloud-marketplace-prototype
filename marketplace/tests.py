from io import StringIO
from django.test import TestCase
from django.core.management import call_command


class ManagementCommandTests(TestCase):
    def test_create_initial_products_works(self):
        out = StringIO()
        call_command('create_initial_products', stdout=out)
        self.assertIn('Created Favro.', out.getvalue())

        out = StringIO()
        call_command('create_initial_products', stdout=out)
        self.assertIn('Favro already exists.', out.getvalue())
