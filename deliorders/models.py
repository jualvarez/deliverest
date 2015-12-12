# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from datetime import date

from django.utils.translation import ugettext_lazy as _
from delicontacts.models import Customer, CONTACT_MODE_CHOICES
from deliproducts.models import Price
from delidelivery.models import DeliveryMethod
from deliorders import utils


ORDER_STATUS_CHOICES = (
        (10, _(u'Iniciada por el usuario')),
        (20, _(u'Confirmada por el usuario')),
        (100, _(u'Abierto')),
        (200, _(u'Cerrado')),
        (300, _(u'Entregado')),
        (400, _(u'Pagado pero no entregado')),
        (500, _(u'Entregado pero no pagado')),
        (600, _(u'Conciliado')),
    )

DELIVERED_STATUSES = (300, 500)

class OrderManager(models.Manager):
    def get_active(self, customer):
        """Try to get an unprocessed order for a customer."""
        try:
            o = Order.objects.get(customer=customer, status__in=[10,20])
        except ObjectDoesNotExist:
            o = None
        return o


class Order(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(u'código'))
    customer = models.ForeignKey(
        Customer,
        verbose_name=_(u'cliente'))
    contact_mode = models.IntegerField(
        choices=CONTACT_MODE_CHOICES,
        blank=True,
        verbose_name=_(u'forma de contacto'))
    delivery_method = models.ForeignKey(
        DeliveryMethod,
        blank=True,
        verbose_name=_(u'método de envío'))
    delivery_address = models.TextField(verbose_name=_(u'dirección de envío'))
    delivery_date = models.DateField(
        verbose_name=_(u"fecha de entrega"),
        blank=True)
    comments = models.TextField(verbose_name=_(u'notas'), blank=True)
    when_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u'fecha de pedido'))
    status = models.IntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=100,
        verbose_name=_(u'estado'))
    reconciled = models.BooleanField(
        default=False,
        verbose_name=_(u'conciliado'))
    when_closed = models.DateField(
        null=True,
        verbose_name=_(u'fecha de cierre'))
    when_delivered = models.DateField(
        null=True,
        verbose_name=_(u'fecha de entrega'))

    objects = OrderManager()

    class Meta:
        verbose_name = _(u'pedido')
        verbose_name_plural = _(u'pedidos')

    def __str__(self):
        return "%s: %s (%s)" % (
            self.code,
            self.customer,
            self.when_create.strftime('%d/%m/%Y'))

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_id = Order.objects.aggregate(models.Max('id'))['id__max'] or 0
            current_id = last_id + 1
            year = date.today().strftime('%y')
            self.code = "P-" + str(year) + "-" + str(current_id).zfill(5)
        # Calculate closing dates automatically
        if self.when_closed is None and self.status > 100:
            self.when_closed = date.today()
        if self.when_delivered is None and self.status in DELIVERED_STATUSES:
            self.when_delivered = date.today()

        # Customer's prefered delivery method is default
        self.delivery_method = self.delivery_method or self.customer.prefered_delivery_method
        # Customer's default contact mode is default
        self.contact_mode = self.contact_mode or self.customer.contact_mode
        # Customer's default address is default
        self.delivery_address = self.delivery_address or self.customer.address

        # Calculate next delivery date
        self.delivery_date = self.delivery_date or date.today() + datetime.timedelta( (self.delivery_method.delivery_day-date.today().weekday()) % 7 )

        # If the order is closed, send notification email to user
        old_status = 0
        if self.pk:
            old_value = Order.objects.get(pk=self.pk)
            old_status = old_value.status
        if old_status < 200 and self.status >= 200:
            self.send_close_email()

        return super(Order, self).save(*args, **kwargs)

    def get_order_total(self):
        total = self.orderitem_set.aggregate(total=models.Sum('sell_price',field='quantity*sell_price'))['total']
        return total if total is not None else 0

    def user_can_open(self):
        # Check if delivery date is open
        open_delivery = self.delivery_date >= utils.next_open_day(date.today(), self.delivery_method.delivery_day)
        # User can only open if they closed it and the target delivery date is still open
        return self.status == 20 and open_delivery

    def send_close_email(self):
        absolute_url = settings.ABSOLUTE_URL
        message = "Need an HTML enabled email client" #render_to_string("email/order_email.txt", {'order':self})
        html_message = render_to_string("email/order_email.html", {'url':absolute_url, 'order': self})
        send_mail(
            subject="Tu pedido está confirmado",
            from_email="Pedidos Organicos de mi Tierra <pedidos@organicosdemitierra.com>",
            message=message,
            html_message=html_message,
            recipient_list=["jualvarez@gmail.com",]
        )

    get_order_total.short_description = _(u"Total de pedido")


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    quantity = models.IntegerField(verbose_name=_(u'cantidad'))
    product = models.ForeignKey(Price, verbose_name=_(u'producto'))
    sell_price = models.DecimalField(max_digits=20, decimal_places=4,
        blank=True,
        verbose_name=_(u'precio de venta (si difiere)'))
    comments = models.CharField(max_length=200, verbose_name='Notas',
        blank=True)

    class Meta:
        verbose_name = _(u'ítem de pedido')
        verbose_name_plural = _(u'ítems de pedido')

    def __str__(self):
        return "%s: %d * $%.2f = $%.2f" % (self.product,
            self.quantity, self.item_sell_price(), self.item_total())

    def save(self, *args, **kwargs):
        self.sell_price = self.sell_price or self.product.sell_price
        return super(OrderItem, self).save(*args, **kwargs)

    def item_sell_price(self):
        return self.sell_price if self.sell_price is not None else self.product.sell_price

    def item_total(self):
        return self.item_sell_price() * self.quantity

    def display(self):
        price = self.product
        product = price.product
        presentation = price.presentation
        presentation_disp = presentation.name if self.quantity == 1 else presentation.plural_name
        return _("{presentation} de {product} ({presentation_unit})").format(presentation=presentation_disp, product=product.name, presentation_unit=presentation.unit_display())
