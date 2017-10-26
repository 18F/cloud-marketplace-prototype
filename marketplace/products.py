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


class Favro(Product):
    slug = 'favro'
    name = 'Favro'


class Mural(Product):
    slug = 'mural'
    name = 'Mural'


class Trello(Product):
    slug = 'trello'
    name = 'Trello'


class Zoom(Product):
    slug = 'zoom'
    name = 'Zoom'
