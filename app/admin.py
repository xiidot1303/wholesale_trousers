from django.contrib import admin
from app.models import *
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, BigIntegerField
from app.forms import SaleItemForm
from django.utils.html import format_html


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('title', 'region')
    search_fields = ('title', 'region')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'manufacturer', 'measurement', 'quantity_in_pack')
    list_filter = ('manufacturer', 'measurement')
    search_fields = ('title',)


class IncomeItemAdmin(admin.TabularInline):
    model = IncomeItem
    extra = 100


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    list_filter = ('datetime',)
    inlines = [IncomeItemAdmin]


@admin.register(ProductBalance)
class ProductBalanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'product_measurement', 'quantity_in_pieces')
    search_fields = ('product__title',)

    def product_measurement(self, obj):
        return obj.product.get_measurement_display()
    product_measurement.short_description = 'Measurement'

    def quantity_in_pieces(self, obj):
        if (obj.product.measurement == 'pack'):
            return obj.quantity * obj.product.quantity_in_pack
        return obj.quantity
    quantity_in_pieces.short_description = 'Donada'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 3
    

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 100
    form = SaleItemForm


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 100


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'store', 'datetime')
    list_filter = ('datetime',)
    search_fields = ('product__title',)

    fieldsets = (
        ('', {
            'fields': ['product', 'quantity', 'store'],
            'description': 'Mahsulot miqdorini kiriting',
        }),
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('store', 'client', 'price', 'datetime', 'remaining_debt', 'products_and_quantities', 'is_checked', 'edit_button')
    list_filter = ('store', 'datetime')
    sortable_by = ('store', 'client', 'price', 'datetime', 'remaining_debt')
    search_fields = ('client__name', 'store__title')
    inlines = [SaleItemInline, PaymentInline, ReturnItemInline]
    list_display_links = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_payments=Sum('payment__amount'),
            remaining_debt=ExpressionWrapper(
                F('price') - F('total_payments'),
                output_field=BigIntegerField()
            )
        )
        return queryset

    def remaining_debt(self, obj):
        return obj.remaining_debt
    remaining_debt.short_description = 'Qolgan qarz'
    remaining_debt.admin_order_field = 'remaining_debt'

    def products_and_quantities(self, obj):
        sale_items = SaleItem.objects.filter(sale=obj)
        return format_html(
            '<br>'.join([f'{item.product.title}: {item.quantity}{item.product.get_measurement_display()[0].lower()} {item.product.quantity_in_pack}x' for item in sale_items])
        )
    products_and_quantities.short_description = 'Mahsulotlar va miqdorlar'

    def edit_button(self, obj):
        return format_html(
            '<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i></a>',
            f'/admin/app/sale/{obj.id}/change/'
        )
    edit_button.short_description = ''
    edit_button.allow_tags = True


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    change_list_template = "admin/app/archive/change_list.html"
    autocomplete_fields = ['product']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_button'] = True
        extra_context['products'] = Product.objects.all()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DailyProductBalance)
class DailyProductBalanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'date')
    search_fields = ('product__title',)
    list_filter = ('product', 'date')


admin.site.site_header = _("Admin panel")
admin.site.site_title = _("Admin")
