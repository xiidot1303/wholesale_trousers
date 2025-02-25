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


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('store', 'client', 'price', 'datetime', 'remaining_debt', 'edit_button')
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


admin.site.site_header = _("Admin panel")
admin.site.site_title = _("Admin")
