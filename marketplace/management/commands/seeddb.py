from django.core.management.base import BaseCommand, CommandError
from marketplace.models import Product
from marketplace.tests import factories

products = [
    factories.FavroFactory.build(),
    factories.MuralFactory.build(),
    factories.TrelloFactory.build(),
    factories.ZoomFactory.build(),
]


class Command(BaseCommand):
    help = 'Creates initial products in the marketplace'

    def handle(self, *args, **options):
        for product in products:
            if Product.objects.filter(slug=product.slug).first():
                self.stdout.write(f'{product.name} already exists.')
            else:
                product.save()
                self.stdout.write(f'Created {product.name}.')
