# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from import_export.admin import ExportMixin
from import_export import resources

from .models import Customer
from deliorders.admin import DefaultListFilter


class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer
        exclude = ('id', 'person_ptr', 'phone', 'contact_mode', 'prefered_delivery_method', 'last_confirmed_tf', 'associated_user')
        export_order = ('name', 'email', 'subscribed_to_newsletter', 'address')


class HasEmailListFilter(admin.SimpleListFilter):

    title = _('tiene email')
    parameter_name = 'has_email'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes' or not self.value():
            queryset = queryset.filter(email__isnull=False).exclude(email='')

        if self.value() == 'no':
            queryset = queryset.filter(Q(email__isnull=True) | Q(email__exact=''))

        return queryset

    def default_value(self):
        return 'yes'

    def choices(self, cl):
        yield {
            'selected': self.value() == '_all',
            'query_string': cl.get_query_string({self.parameter_name: '_all'}, []),
            'display': _(u'All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (self.value() == None and force_text(self.default_value()) == force_text(lookup)),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


class NewsLetterFilter(DefaultListFilter):

    title = _('suscripto al newsletter')
    parameter_name = 'subscribed_to_newsletter__exact'

    def default_value(self):
        return 1

    def lookups(self, request, model_admin):
        return (
            (1, _('Yes')),
            (0, _('No')),
        )


class CustomerAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ['name', 'email', 'address']
    list_display = ('name', 'address', 'email', 'phone', 'subscribed_to_newsletter')
    list_filter = (NewsLetterFilter, HasEmailListFilter)

    # Export
    resource_class = CustomerResource


admin.site.register(Customer, CustomerAdmin)
