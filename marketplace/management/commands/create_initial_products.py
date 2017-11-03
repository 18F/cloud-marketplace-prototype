from django.core.management.base import BaseCommand, CommandError
from marketplace.models import Product

products = []

products.append(Product(
    slug = 'favro',
    name = 'Favro',
    category = "Project management",
    description = """
        Favro is a planning and collaboration app which enables
        developers, designers, and clients to all stay on the same
        page and track progress.
    """,
))

products.append(Product(
    slug = 'mural',
    name = 'Mural',
    category = "Live collaboration",
    description = """
        A web-based solution for small teams that need a virtual
        workspace in which they can brainstorm, plan and collaborate.
    """,
))


products.append(Product(
    slug = 'trello',
    name = 'Trello',
    category = "Project management",
    description = """
        This is a card-based tool for managing projects and tasks.
        It uses customizable Kanban-style boards, and offers
        "power ups" such as GitHub integration.
    """,
))


products.append(Product(
    slug = 'zoom',
    name = 'Zoom',
    category = "Video conferencing",
    description = """
        This is a video conferencing tool with features such as chat,
        screen sharing, and session recording. No account is required
        to participate in conferences.
    """
))


class Command(BaseCommand):
    help = 'Creates initial products in the marketplace'

    def handle(self, *args, **options):
        for product in products:
            if Product.objects.filter(slug=product.slug).first():
                self.stdout.write(f'{product.name} already exists.')
            else:
                product.save()
                self.stdout.write(f'Created {product.name}.')
