from django.contrib import admin

from .models import Product, Team, LicenseType


class LicenseTypeInline(admin.TabularInline):
    model = LicenseType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        LicenseTypeInline,
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
