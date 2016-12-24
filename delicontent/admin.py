# -*- coding: utf-8 -*-

from django.contrib import admin

from delicontent.models import Page, PromoImage


class PageAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ('title', 'show_in_nav', 'order')
    list_editable = ('show_in_nav', 'order')
    list_filter = ('show_in_nav',)


class PromoImageAdmin(admin.ModelAdmin):
    search_fields = ['description', ]
    list_display = ('description',)
    list_filter = ('is_active',)


admin.site.register(Page, PageAdmin)
admin.site.register(PromoImage, PromoImageAdmin)
