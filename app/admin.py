from django.contrib import admin
from app.models import *
from django.utils.translation import gettext_lazy as _


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('title', 'region')
    search_fields = ('title', 'region')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'manufacturer', 'measurement', 'quantity_in_pack')
    list_filter = ('manufacturer', 'measurement')
    search_fields = ('title',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'datetime')
    list_filter = ('datetime',)
    search_fields = ('product__title',)


@admin.register(ProductBalance)
class ProductBalanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__title',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 100


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('store', 'client', 'datetime')
    list_filter = ('store', 'datetime')
    search_fields = ('client__name', 'store__title')
    inlines = [SaleItemInline]


admin.site.site_header = _("Admin panel")
admin.site.site_title = _("Admin")
