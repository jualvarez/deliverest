# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from markdownx.models import MarkdownxField

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


class ActiveManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return super(ActiveManager, self).all().filter(is_active=True)


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(
        verbose_name=_(u'nombre'),
        max_length=150,
        unique=True)
    slug = models.SlugField(
        max_length=50,
        verbose_name=_(u'direccion web'),
        unique=True,
        null=True)
    order = models.PositiveIntegerField(verbose_name=_('orden'), null=True)
    is_active = models.BooleanField(verbose_name=_('activo'), default=True)
    parent = models.ForeignKey(
        'self',
        verbose_name=(u'categoría padre'),
        related_name='subcategories',
        null=True,
        blank=True)

    color = models.CharField(
        verbose_name=_(u'color'),
        help_text=_(u'color de identificación de la categoría'),
        max_length=8,
        null=True,
        blank=True)
    children_color = models.CharField(
        verbose_name=_(u'color de los hijos'),
        help_text=_(u'color de identificación para los '
                    u'hijos de esta categoría'),
        max_length=8,
        null=True,
        blank=True)

    objects = ActiveManager()

    class Meta:
        verbose_name = _(u'categoría')
        verbose_name_plural = _(u'categorías')
        ordering = ('order',)

    def parent_crumbs(self, instance=None, crumb_str=None):
        if instance is None:
            instance = self
            crumb_str = self.name

        if instance.parent is not None:
            crumb_str = u"%s > %s" % (instance.parent.name, crumb_str)
            return self.parent_crumbs(instance.parent, crumb_str)

        else:
            return crumb_str

    def get_absolute_url(self):
        return reverse(
            'deliorders.views.home',
            kwargs={'category': self.slug})

    def __str__(self):
        return self.parent_crumbs()


@python_2_unicode_compatible
class Presentation(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name=_(u'nombre'))
    plural_name = models.CharField(
        max_length=150,
        verbose_name=_(u'plural'))
    quantifiable = models.BooleanField(
        default=True,
        verbose_name=_(u'cuantificable'))
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_(u'cantidad'),
        blank=True,
        null=True)
    measure_unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _(u'presentación')
        verbose_name_plural = _(u'presentaciones')
        unique_together = ('name', 'quantity', 'measure_unit')
        ordering = ('name', 'quantity', 'measure_unit')

    def __str__(self):
        if self.quantity is not None:
            return u"%s de %s %s" % (
                self.name,
                self.quantity if self.quantity.to_integral() - self.quantity else self.quantity.to_integral(),
                self.get_measure_unit_display() if (self.quantity == 1) or (self.measure_unit not in UNIT_CHOICES_PLURAL) else UNIT_CHOICES_PLURAL[self.measure_unit])
        else:
            return self.name

    @cached_property
    def plural_repr(self):
        if self.quantity is not None:
            return u"%s de %s %s" % (
                self.plural_name,
                self.quantity if self.quantity.to_integral() - self.quantity else self.quantity.to_integral(),
                self.get_measure_unit_display() if (self.quantity == 1) or (self.measure_unit not in UNIT_CHOICES_PLURAL) else UNIT_CHOICES_PLURAL[self.measure_unit])
        else:
            return self.plural_name

    def unit_display(self):
        if self.quantity is not None:
            return "%0.f %s" % (
                self.quantity,
                self.get_measure_unit_display() if (self.quantity == 1) or (self.measure_unit not in UNIT_CHOICES_PLURAL) else UNIT_CHOICES_PLURAL[self.measure_unit])
        else:
            return self.name


@python_2_unicode_compatible
class Product(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name=_(u'nombre'),
        unique=True
    )
    description = models.TextField(verbose_name=_(u'descripción'), help_text=_(u'descripción que se muestra en los listados de producto'), blank=True)
    long_description = MarkdownxField(verbose_name=_(u'descripción larga'), help_text=_(u'descripción que se muestra en el detalle de producto'), blank=True)
    presentations = models.ManyToManyField(Presentation, through='Price')
    provider = models.ForeignKey('Provider', verbose_name=_(u'proveedor'), blank=True, null=True)

    category = models.ForeignKey(
        'Category',
        verbose_name=_(u'categoría'),
        null=True,
        blank=True)
    is_active = models.BooleanField(verbose_name=_(u'activo'), default=True)

    objects = ActiveManager()

    class Meta:
        verbose_name = _(u'producto')
        verbose_name_plural = _(u'productos')
        ordering = ('name',)

    def __str__(self):
        return u"%s" % (self.name)

CURRENCY_CHOICE = (
    ('ARS', _(u'Peso argentino')),
    ('USD', _(u'Dolar'))
)


@python_2_unicode_compatible
class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(u'producto'))
    presentation = models.ForeignKey(
        Presentation,
        verbose_name=_(u'presentación'))
    in_stock = models.BooleanField(
        verbose_name=_(u'en stock'),
        default=True)
    wholesale = models.BooleanField(
        verbose_name=_(u'Por mayor'),
        default=False)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICE,
        default='ARS',
        verbose_name=_(u'moneda'))
    sell_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_(u'precio de venta'))
    buy_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_(u'precio de compra'))
    featured = models.BooleanField(default=False, verbose_name=_(u'destacado'))
    is_active = models.BooleanField(verbose_name=_(u'activo'), default=True)

    objects = ActiveManager()

    class Meta:
        verbose_name = _(u'precio')
        verbose_name_plural = _(u'precios')
        unique_together = ('product', 'presentation', 'wholesale')
        ordering = ('product__name', )

    def __str__(self):
        return u"%s (%s): $%.2f" % (
            self.product.name,
            self.presentation,
            self.sell_price)

    @property
    def slug_id(self):
        from django.utils.text import slugify
        return "{}-{}".format(self.id, slugify(self.product.name))

    def get_absolute_url(self):
        return reverse(
            'price',
            kwargs={'slug_id': self.slug_id}
        )


@python_2_unicode_compatible
class Provider(models.Model):
    code = models.CharField(max_length=50, verbose_name=_(u'código'))
    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))
    address = models.TextField(verbose_name=_(u'dirección'), blank=True)
    phone = models.CharField(
        max_length=100,
        verbose_name=_(u'teléfono'),
        blank=True)

    class Meta:
        verbose_name = _(u'proveedor')
        verbose_name_plural = _(u'proveedores')
        ordering = ('name',)

    def __str__(self):
        return u"%s (%s)" % (self.name, self.code)
