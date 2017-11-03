from django.contrib import admin

from .models import Product, Team


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
