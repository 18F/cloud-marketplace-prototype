from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (Product, Team, LicenseType, Purchase,
                     LicenseRequest, UserMarketplaceInfo)

class MarketplaceInfoInline(admin.StackedInline):
    verbose_name_plural = 'Marketplace Info'
    model = UserMarketplaceInfo
    can_delete = False


class MarketplaceUserAdmin(UserAdmin):
    inlines = (MarketplaceInfoInline,)


admin.site.unregister(User)
admin.site.register(User, MarketplaceUserAdmin)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('license_type', 'team', 'license_count', 'start_date',
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


@admin.register(LicenseRequest)
class LicenseRequestAdmin(admin.ModelAdmin):
    list_display = ('license_type', 'user', 'created_at', 'updated_at',
                    'status', 'is_self_reported')
