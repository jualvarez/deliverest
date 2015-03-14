# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

UNIT_L = 'L'
UNIT_ML = 'CC'
UNIT_G = 'G'
UNIT_KG = 'KG'
UNIT_UNIT = 'U'

UNIT_CHOICES = (
        (UNIT_L, _(u'litro')),
        (UNIT_ML, _(u'cc')),
        (UNIT_G, _(u'gramo')),
        (UNIT_KG, _(u'kilogramo')),
        (UNIT_UNIT, _(u'unidad'))
    )

UNIT_CHOICES_PLURAL = {
        UNIT_L: _(u'litros'),
        UNIT_G: _(u'gramos'),
        UNIT_KG: _(u'kilogramos'),
        UNIT_UNIT: _(u'unidades')
    }


class Presentation(models.Model):

    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))
    quantifiable = models.BooleanField(default=True, verbose_name=_(u'cuantificable'))
    quantity = models.DecimalField(max_digits=6, decimal_places=2,
        verbose_name=_(u'cantidad'), blank=True, null=True)
    measure_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = _(u'presentación')
        verbose_name_plural = _(u'presentaciones')
        unique_together = ('name', 'quantity', 'measure_unit')

    def __str__(self):
        if self.quantity != None:
            return "%s %s %s" % (self.name, self.quantity,
                    self.get_measure_unit_display() if (self.quantity == 1) or (self.measure_unit not in UNIT_CHOICES_PLURAL) else UNIT_CHOICES_PLURAL[self.measure_unit])
        else:
            return self.name


class Product(models.Model):

    name = models.CharField(max_length=200, verbose_name=_(u'nombre'), unique=True)
    description = models.CharField(max_length=500,
        verbose_name=_(u'descripción'))
    presentations = models.ManyToManyField(Presentation, through='Price')
    provider = models.ForeignKey('Provider', blank=True, null=True)

    class Meta:
        verbose_name = _(u'producto')
        verbose_name_plural = _(u'productos')

    def __str__(self):
        return "%s" % (self.name)

CURRENCY_CHOICE = (
    ('ARS', _(u'Peso argentino')),
    ('USD', _(u'Dolar'))
    )


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(u'producto'))
    presentation = models.ForeignKey(Presentation,
        verbose_name=_(u'presentación'))
    wholesale = models.BooleanField(verbose_name=_(u'Por mayor'), default=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE,
        default='ARS', verbose_name=_(u'moneda'))
    sell_price = models.DecimalField(max_digits=20, decimal_places=4,
        verbose_name=_(u'precio de venta'))
    buy_price = models.DecimalField(max_digits=20, decimal_places=4,
        verbose_name=_(u'precio de compra'))

    class Meta:
        verbose_name = _(u'precio')
        verbose_name_plural = _(u'precios')
        unique_together = ('product', 'presentation', 'wholesale')

    def __str__(self):
        return "%s (%s): $%.2f" % (self.product.name,
                            self.presentation, self.sell_price)


class Provider(models.Model):
    code = models.CharField(max_length=50, verbose_name=_(u'código'))
    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))
    address = models.TextField(verbose_name=_(u'dirección'), blank=True)
    phone = models.CharField(max_length=100, verbose_name=_(u'teléfono'),
        blank=True)

    class Meta:
        verbose_name = _(u'proveedor')
        verbose_name_plural = _(u'proveedores')

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)