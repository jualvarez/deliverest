# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import DeliveryMethod


class DeliveryMethodAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ('code', 'name', 'delivery_day', 'delivery_time', 'is_delivery', 'delivery_price')
    list_editable = ('delivery_day', 'delivery_time','is_delivery', 'delivery_price')

admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
