from decimal import Decimal

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q, Sum
from django.template import RequestContext
from django.conf.urls import url, patterns
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Order, OrderItem
from delidelivery.models import DeliveryMethod


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdminChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(OrderAdminChangeList, self).get_results(*args, **kwargs)
        self.order_sum = Decimal(0.0)
        for order in self.result_list.all():
            self.order_sum = self.order_sum + order.get_order_total()

class OrderAdmin(admin.ModelAdmin):
    exclude = ('code', 'when_closed', 'when_delivered', 'reconciled')
    search_fields = ('code', 'customer__first_name', 'customer__last_name')
    list_display = ('code', 'customer', 'get_contact_mode', 'delivery_method', 'get_order_total',
        'get_customer_address', 'get_customer_phone', 'delivery_date', 'when_create', 'status')
    list_filter = ('status', 'delivery_method')
    inlines = [OrderItemInline]
    actions = ['close_orders', 'deliver_orders', 'reconcile_orders', 'balance_report']

    def get_changelist(self, request):
        return OrderAdminChangeList

    def get_contact_mode(self, obj):
        return obj.customer.email if (obj.contact_mode == 100 and obj.customer.email) else obj.get_contact_mode_display()
    get_contact_mode.admin_order_field = 'customer'
    get_contact_mode.short_description = _('Contacto')

    def get_customer_address(self, obj):
        return obj.customer.address
    get_customer_address.admin_order_field = 'customer'
    get_customer_address.short_description = _('Dirección de entrega')

    def get_customer_phone(self, obj):
        return obj.customer.phone
    get_customer_phone.admin_order_field = 'customer'
    get_customer_phone.short_description = _('Teléfono de contacto')

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
                    item_display = "%s (%s)" % (
                        prod.product.name,
                        prod.presentation
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

    def balance_report(self, request, queryset):
        results = {}
        totals = [0, 0, 0, 0, 0]
        for order in queryset:
            for item in order.orderitem_set.all():
                try:
                    edit_item = results[item.product.pk]
                except KeyError:
                    prod = item.product
                    item_display = "%s (%s)" % (
                        prod.product.name,
                        prod.presentation
                    )
                    results[item.product.pk] = [item_display] + [0, 0, 0, 0]
                
                quantity = item.quantity
                cost = item.product.buy_price * quantity
                sell_price = item.sell_price * quantity
                profit = sell_price - cost

                results[item.product.pk][1] += quantity
                results[item.product.pk][2] += cost
                results[item.product.pk][3] += sell_price
                results[item.product.pk][4] += profit

                totals[1] += quantity
                totals[2] += cost
                totals[3] += sell_price
                totals[4] += profit

        return render_to_response(self.order_balance_template, {
                'title': _('Balance'),
                'results': results,
                'totals': totals
            }, context_instance=RequestContext(request))

    def change_orders_status(self, queryset, from_status, to_status):
        if hasattr(from_status, '__contains__'):
            compare = from_status
        else:
            compare = (from_status,)

        for order in queryset:
            if order.status in compare:
                order.status = to_status
                order.save()

    def close_orders(self, request, queryset):
        self.change_orders_status(queryset, 100, 200)

    def deliver_orders(self, request, queryset):
        self.change_orders_status(queryset, 200, 300)

    def reconcile_orders(self, request, queryset):
        self.change_orders_status(queryset, (300,400), 600)

    close_orders.short_description = _("Cerrar pedidos")
    deliver_orders.short_description = _("Marcar pedidos entregados")
    balance_report.short_description = _("Balance de pedidos")
    reconcile_orders.short_description = _("Conciliar pedidos")

    order_report_template = 'admin/products_report.html'
    order_print_template = 'admin/orders_print.html'
    order_balance_template = 'admin/orders_balance.html'

admin.site.register(Order, OrderAdmin)
