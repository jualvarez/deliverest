# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name','email','address']
    list_display = ('name', 'address', 'email', 'phone')
    #list_filter = ('prefered_delivery_method__name',)

admin.site.register(Customer, CustomerAdmin)