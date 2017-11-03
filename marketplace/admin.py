from django.contrib import admin

from .models import Product, Team, LicenseType, Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('license_type', 'license_count', 'start_date',
                    'end_date')


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
