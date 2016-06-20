# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import DeliveryMethod


class DeliveryMethodAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ('code', 'name', 'delivery_price', 'is_delivery')
    list_editable = ('delivery_price', 'is_delivery')

admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
