# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from deliorders import utils
from .models import Category, Presentation, Product, Price, Provider


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')

admin.site.register(Category, CategoryAdmin)


class ProviderAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ('code', 'name')

admin.site.register(Provider, ProviderAdmin)


class PresentationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'quantity', 'measure_unit')
    list_filter = ('name', 'measure_unit')

admin.site.register(Presentation, PresentationAdmin)


class ApplyProductCategory(object):
    """
    Action class to move products in queryset to
    a specified category defined in class
    initialization
    """
    def __init__(self, category):
        self.category = category

    def __call__(self, obj, request, queryset):
        for prod in queryset:
            prod.category = self.category
            prod.save()

    @property
    def short_description(self):
        return _(u'Aplicar a categoría "%s"' % self.category)

    @property
    def name(self):
        return u'apply_cat_%s' % self.category.name


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ('name', 'description', 'category', 'is_active')
    list_editable = ('category', 'is_active')
    list_filter = ('category',)

    def get_actions(self, request):
        actions = super(ProductAdmin, self).get_actions(request)
        category_actions_list = [ApplyProductCategory(cat) for cat in Category.objects.all()]
        category_actions = dict((action.name, (action, action.name, action.short_description)) for action in category_actions_list)

        # Other actions
        def add_as_featured_product(self, request, queryset):
            for product in queryset:
                product.featured = True
                product.save()
        additional_actions = {}
        additional_actions['add_as_featured_product'] = (add_as_featured_product, 'add_as_featured_product', _('Agregar como producto destacado'))
        actions.update(category_actions)
        actions.update(additional_actions)
        return actions

admin.site.register(Product, ProductAdmin)


class PriceAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'product__description', 'presentation__name']
    list_display = ('product', 'presentation', 'currency', 'sell_price', 'buy_price', 'is_active', 'featured')
    list_editable = ('sell_price', 'buy_price', 'is_active', 'featured')
    list_filter = ('product__category', 'presentation__name',)
    list_per_page = 25
    ordering = ('product__name',)
    actions = ['build_email']

    def build_email(self, request, queryset):
        def closing_date():
            tf_start, tf_end = utils.tf_frame()
            return tf_start

        def delivery_dates():
            start, end = utils.delivery_days(timezone.now())
            delivery_dates = [start, end]
            return delivery_dates

        def delivery_cost():
            return u"%.2f" % settings.DELIVERY_DEFAULT_PRICE

        queryset.order_by('product__name')
        categories = []
        products = {}

        for price in queryset:
            if price.product.category is None:
                category_name = _(u'Otros')
            else:
                category_name = price.product.category.name
            if category_name not in categories:
                categories.append(category_name)
                products[category_name] = []
            products[category_name].append(price)

        categories = sorted(categories)
        if _(u'Otros') in categories:
            categories.remove(_(u'Otros'))
            categories.append(_(u'Otros'))

        return render_to_response(self.email_output_template, {
            'title': _(u'Email a enviar'),
            'categories': categories,
            'products': products,
            'closing_date': closing_date,
            'delivery_dates': delivery_dates,
            'delivery_cost': delivery_cost,
        }, context_instance=RequestContext(request))

    build_email.short_description = _(u'Armar e-mail a enviar con productos seleccionados')
    email_output_template = 'admin/email_output.html'

admin.site.register(Price, PriceAdmin)
