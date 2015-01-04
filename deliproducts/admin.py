from django.contrib import admin
from .models import Presentation, Product, Price, Provider


class ProviderAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ('code', 'name')

admin.site.register(Provider, ProviderAdmin)


class PresentationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'quantity', 'measure_unit')

admin.site.register(Presentation, PresentationAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ('name', 'description')

admin.site.register(Product, ProductAdmin)


class PriceAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'product__description','presentation__name']
    list_display = ('product', 'presentation', 'currency', 'sell_price', 'buy_price')
    list_filter = ('presentation', 'sell_price', 'buy_price')

admin.site.register(Price, PriceAdmin)
