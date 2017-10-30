import abc
from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


MAX_SLUG_LENGTH = 50

def get_all():
    # TODO: Consider caching the return value.
    instances = []
    for classname in settings.MARKETPLACE_PRODUCTS:
        cls = import_string(classname)
        instances.append(cls())
    return instances


def get_all_choices():
    return [
        (product.slug, product.name)
        for product in get_all()
    ]


class Product(metaclass=abc.ABCMeta):
    # Subclasses must define these.
    slug = None
    name = None
    category = None
    description = None

    @property
    def icon(self):
        return staticfiles_storage.url(
            f"marketplace/products/{self.slug}/icon.png")


    @property
    def primary_screenshot(self):
        return staticfiles_storage.url(
            f"marketplace/products/{self.slug}/primary_screenshot.png")


    @property
    def detail_url(self):
        return reverse('product_detail', kwargs={'product': self})


class Favro(Product):
    slug = 'favro'
    name = 'Favro'
    category = "Project management"

    description = """
        Favro is a planning and collaboration app which enables
        developers, designers, and clients to all stay on the same
        page and track progress.
    """


class Mural(Product):
    slug = 'mural'
    name = 'Mural'
    category = "Live collaboration"

    description = """
        A web-based solution for small teams that need a virtual
        workspace in which they can brainstorm, plan and collaborate.
    """


class Trello(Product):
    slug = 'trello'
    name = 'Trello'
    category = "Project management"

    description = """
        This is a card-based tool for managing projects and tasks.
        It uses customizable Kanban-style boards, and offers
        "power ups" such as GitHub integration.
    """


class Zoom(Product):
    slug = 'zoom'
    name = 'Zoom'
    category = "Video conferencing"

    description = """
        This is a video conferencing tool with features such as chat,
        screen sharing, and session recording. No account is required
        to participate in conferences.
    """
