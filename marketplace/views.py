from django.shortcuts import render
import django.contrib.auth


def home(request):
    return render(request, 'marketplace/home.html')

def logout(request):
    django.contrib.auth.logout(request)
    return render(request, 'marketplace/logged_out.html')

def product_detail(request, product):
    raise NotImplementedError(f"TODO: Implement page for {product.name}!")
