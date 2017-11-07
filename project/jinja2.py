from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

from marketplace.models import Product, LicenseRequest


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'Product': Product,
        'LicenseRequest': LicenseRequest,
    })
    return env
