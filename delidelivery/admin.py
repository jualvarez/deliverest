from django.contrib import admin
from .models import DeliveryMethod


class DeliveryMethodAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ('code', 'name')

admin.site.register(DeliveryMethod, DeliveryMethodAdmin)