from .models import Product


class ProductConverter:
    regex = '[A-Za-z0-9_\-]+'

    def to_python(self, value):
        product = Product.objects.filter(slug=value).first()
        if product:
            return product
        raise ValueError(f'No product slug matching "{value}"')

    def to_url(self, value):
        return value.slug
