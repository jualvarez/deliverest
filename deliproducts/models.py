from django.db import models
from django.utils.translation import ugettext_lazy as _

UNIT_L = 'L'
UNIT_ML = 'ML'
UNIT_G = 'G'
UNIT_KG = 'KG'
UNIT_UNIT = 'U'

UNIT_CHOICES = (
        (UNIT_L, _('litro')),
        (UNIT_ML, _('mililitro')),
        (UNIT_G, _('gramo')),
        (UNIT_KG, _('kilogramo')),
        (UNIT_UNIT, _('unidad'))
    )


class Presentation(models.Model):

    name = models.CharField(max_length=150, verbose_name=_('nombre'))
    quantity = models.DecimalField(max_digits=6, decimal_places=2,
        verbose_name=_('cantidad'))
    measure_unit = models.CharField(max_length=2, choices=UNIT_CHOICES)

    class Meta:
        verbose_name = _('presentación')
        verbose_name_plural = _('presentaciones')

    def __str__(self):
        return "%s %s %s" % (self.name, self.quantity,
                    self.get_measure_unit_display())


class Product(models.Model):

    code = models.CharField(max_length=50, unique=True,
        verbose_name=_('codigo'))
    name = models.CharField(max_length=200, verbose_name=_('nombre'))
    description = models.CharField(max_length=500,
        verbose_name=_('descripción'))
    presentations = models.ManyToManyField(Presentation, through='Price')
    provider = models.ForeignKey('Provider')

    class Meta:
        verbose_name = _('producto')
        verbose_name_plural = _('productos')

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

CURRENCY_CHOICE = (
    ('ARS', _('Peso argentino')),
    ('USD', _('Dolar'))
    )


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('producto'))
    presentation = models.ForeignKey(Presentation,
        verbose_name=_('presentación'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE,
        default='ARS', verbose_name=_('moneda'))
    sell_price = models.DecimalField(max_digits=20, decimal_places=4,
        verbose_name=_('precio de venta'))
    buy_price = models.DecimalField(max_digits=20, decimal_places=4,
        verbose_name=_('precio de compra'))

    class Meta:
        verbose_name = _('precio')
        verbose_name_plural = _('precios')
        unique_together = ('product', 'presentation')

    def __str__(self):
        return "%s (%s): $%.2f" % (self.product.name,
                            self.presentation.name, self.sell_price)


class Provider(models.Model):
    code = models.CharField(max_length=50, verbose_name=_('código'))
    name = models.CharField(max_length=150, verbose_name=_('nombre'))
    address = models.TextField(verbose_name=_('dirección'), blank=True)
    phone = models.CharField(max_length=100, verbose_name=_('teléfono'),
        blank=True)

    class Meta:
        verbose_name = _('proveedor')
        verbose_name_plural = _('proveedores')

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)