from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ('first_name', 'delivery_method_name')
    list_filter = ('prefered_delivery_method__name',)

admin.site.register(Customer, CustomerAdmin)