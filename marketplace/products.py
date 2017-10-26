import abc
from django.conf import settings
from django.utils.module_loading import import_string


def get_all():
    instances = []
    for classname in settings.MARKETPLACE_PRODUCTS:
        cls = import_string(classname)
        instances.append(cls())
    return instances


class Product(metaclass=abc.ABCMeta):
    # Subclasses must define these.
    slug = None
    name = None
    description = None


class Favro(Product):
    slug = 'favro'
    name = 'Favro'

    description = """
        Favro is a planning and collaboration app which enables
        developers, designers, and clients to all stay on the same
        page and track progress.
    """


class Mural(Product):
    slug = 'mural'
    name = 'Mural'

    description = """
        A web-based solution for small teams that need a virtual
        workspace in which they can brainstorm, plan and collaborate.
    """


class Trello(Product):
    slug = 'trello'
    name = 'Trello'

    description = """
        This is a card-based tool for managing projects and tasks.
        It uses customizable Kanban-style boards, and offers
        "power ups" such as GitHub integration.
    """


class Zoom(Product):
    slug = 'zoom'
    name = 'Zoom'

    description = """
        This is a video conferencing tool with features such as chat,
        screeen sharing, and session recording. No account is required
        to participate in conferences.
    """
