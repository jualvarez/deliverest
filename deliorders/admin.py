from django.contrib import admin
from django.db.models import Q
from django.template import RequestContext
from django.conf.urls import url, patterns
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Order, OrderItem
from delidelivery.models import DeliveryMethod

import autocomplete_light


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    exclude = ('code', 'when_closed', 'when_delivered', 'reconciled')
    search_fields = ('code', 'customer__first_name', 'customer__last_name')
    list_display = ('code', 'customer', 'delivery_method', 'order_total',
        'delivery_date', 'when_create', 'status')
    list_filter = ('status', 'delivery_method', 'customer')
    inlines = [OrderItemInline]
    actions = ['close_orders']

    form = autocomplete_light.modelform_factory(Order)

    order_report_template = 'admin/products_report.html'
    order_print_template = 'admin/orders_print.html'

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^products_report/$', self.products_report, name='admin_order_products_report'),
            url(r'^print_orders/$', self.print_orders, name='admin_order_print'),
            url(r'^print_orders/(?P<delivery_method_id>[0-9])/$', self.print_orders, name='admin_order_print'),
        )
        return my_urls + urls

    def products_report(self, request):
        # Not-delivered orders
        pending_orders = Order.objects.filter(Q(status=200) | Q(status=400))
        delivery_methods = {dm.pk: dm.name for dm in DeliveryMethod.objects.all().order_by('pk')}
        result_headers = ['Product'] + list(delivery_methods.values()) + ['Total']

        results = {}
        for order in pending_orders:
            for item in order.orderitem_set.all():
                try:
                    edit_item = results[item.product.pk]
                except KeyError:
                    prod = item.product
                    item_display = "%s %s %d %s" % (
                        prod.product.name,
                        prod.presentation.name,
                        prod.presentation.quantity,
                        prod.presentation.measure_unit
                    )
                    results[item.product.pk] = [item_display] + [0 for i in delivery_methods] + [0]
                for pos, delivery_method_id in enumerate(delivery_methods.keys()):
                    if order.delivery_method_id == delivery_method_id:
                        results[item.product.pk][pos + 1] += item.quantity
                results[item.product.pk][-1] += item.quantity

        return render_to_response(self.order_report_template, {
                'title': _('Reporte de cantidades de producto'),
                'result_headers': result_headers,
                'results': results
            }, context_instance=RequestContext(request))

    def print_orders(self, request, delivery_method_id=None):
        pending_orders = Order.objects.filter(Q(status=200) | Q(status=400))
        delivery_methods = DeliveryMethod.objects.all()
        delivery_method = None
        title_append = ""

        if delivery_method_id:
            delivery_method = get_object_or_404(DeliveryMethod,
                                    pk=delivery_method_id)
            pending_orders = pending_orders.filter(
                delivery_method_id=delivery_method_id)
            title_append = _(" para ") + '"' + delivery_method.name + '"'

        return render_to_response(self.order_print_template, {
                'title': _('Ordenes a entregar') + title_append,
                'delivery_method': delivery_method,
                'delivery_methods': delivery_methods,
                'orders': pending_orders
            }, context_instance=RequestContext(request))

    def close_orders(self, request, queryset):
        for order in queryset:
            if order.status == 100:
                order.status = 200
                order.save()

    close_orders.short_description = _("Cerrar órdenes")

admin.site.register(Order, OrderAdmin)