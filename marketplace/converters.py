from . import products


class ProductConverter:
    regex = '[A-Za-z0-9_\-]+'

    def to_python(self, value):
        # TODO: Obviously this isn't very efficient but it'll do
        # for a prototype.
        for product in products.get_all():
            if value == product.slug:
                return product
        raise ValueError(f'No product slug matching "{value}"')

    def to_url(self, value):
        return value.slug
