from django.urls import register_converter, path, include

from . import views, converters

register_converter(converters.ProductConverter, 'product')

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('products/<product:product>/', views.product_detail,
         name='product_detail'),
    path('usage', views.usage, name='usage'),
]
