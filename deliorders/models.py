from django.db import models
from datetime import date
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from delicontacts.models import Customer, CONTACT_MODE_CHOICES
from deliproducts.models import Price
from delidelivery.models import DeliveryMethod


ORDER_STATUS_CHOICES = (
        (100, _('Abierto')),
        (200, _('Cerrado')),
        (300, _('Entregado')),
        (400, _('Pagado pero no entregado')),
        (500, _('Entregado pero no pagado')),
        (600, _('Conciliado')),
    )


class Order(models.Model):
    code = models.CharField(max_length=50, unique=True,
        verbose_name=_('código'))
    customer = models.ForeignKey(Customer, verbose_name=_('cliente'))
    contact_mode = models.IntegerField(choices=CONTACT_MODE_CHOICES, blank=True,
        verbose_name=_('Forma de contacto'))
    delivery_method = models.ForeignKey(DeliveryMethod, blank=True, null=True,
        verbose_name=_('método de envío'))
    delivery_date = models.DateField(default=date.today(),
        verbose_name=_("fecha de entrega"))
    comments = models.TextField(verbose_name=_('notas'), blank=True)
    when_create = models.DateTimeField(auto_now_add=True,
        verbose_name=_('fecha de pedido'))
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=100,
        verbose_name=_('estado'))
    reconciled = models.BooleanField(default=False,
        verbose_name=_('conciliado'))
    when_closed = models.DateField(null=True,
        verbose_name=_("fecha de cierre"))
    when_delivered = models.DateField(null=True,
        verbose_name=_("fecha de entrega"))

    class Meta:
        verbose_name = _('pedido')
        verbose_name_plural = _('pedidos')

    def __str__(self):
        return "%s: %s (%s)" % (self.code,
            self.customer, self.when_create.strftime('%d/%m/%Y'))

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_id = Order.objects.aggregate(models.Max('id'))['id__max'] or 0
            current_id = last_id + 1
            year = date.today().strftime('%y')
            self.code = "P-" + str(year) + "-" + str(current_id).zfill(5)
        # Calculate closing dates automatically
        if self.when_closed is None and self.status > 100:
            self.when_closed = date.today()
        if self.when_delivered is None and self.status in (300, 500):
            self.when_delivered = date.today()

        # Customer's prefered delivery method is default
        self.delivery_method = self.delivery_method or self.customer.prefered_delivery_method
        # Customer's default contact mode is default
        self.contact_mode = self.contact_mode or self.customer.contact_mode

        return super(Order, self).save(*args, **kwargs)

    def order_total(self):
        return self.orderitem_set.aggregate(total=models.Sum('sell_price',field='quantity*sell_price'))['total']


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Price, verbose_name=_('producto'))
    sell_price = models.DecimalField(max_digits=20, decimal_places=4,
        blank=True,
        verbose_name=_('precio de venta (si difiere)'))
    quantity = models.IntegerField(verbose_name=_('cantidad'))
    comments = models.CharField(max_length=200, verbose_name='Notas',
        blank=True)

    class Meta:
        verbose_name = _('ítem de pedido')
        verbose_name_plural = _('ítems de pedido')

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