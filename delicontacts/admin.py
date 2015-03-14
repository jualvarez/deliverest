from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ('name', 'address', 'phone', 'delivery_method_name')
    list_filter = ('prefered_delivery_method__name',)

admin.site.register(Customer, CustomerAdmin)