from django.contrib import admin

from delicontent.models import PromoImage

class PromoImageAdmin(admin.ModelAdmin):
    search_fields = ['description',]
    list_display = ('description',)
    list_filter = ('is_active',)

admin.site.register(PromoImage, PromoImageAdmin)