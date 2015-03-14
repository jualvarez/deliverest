# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from delidelivery.models import DeliveryMethod

CONTACT_MODE_CHOICES = (
        (100, _(u'E-mail')),
        (200, _(u'Facebook')),
        (300, _(u'Telefono')),
        (400, _(u'Otro')),
    )

class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u'nombre'))
    email = models.EmailField(verbose_name=_(u'e-mail'), blank=True)
    address = models.TextField(blank=True, verbose_name=_(u'dirección'))
    phone = models.CharField(max_length=200, blank=True,
        verbose_name=_(u'teléfono'))

    class Meta:
        verbose_name = _(u'persona')
        verbose_name_plural = _(u'personas')
        ordering = ('name',)

    def __str__(self):
        return "%s" % (self.name)


class Customer(Person):
    contact_mode = models.IntegerField(choices=CONTACT_MODE_CHOICES, default=100, verbose_name=_(u'Forma de contacto'))
    prefered_delivery_method = models.ForeignKey(DeliveryMethod,
        verbose_name=_(u'método de envio preferido'))

    class Meta:
        verbose_name = _(u'cliente')
        verbose_name_plural = _(u'clientes')

    def __str__(self):
        return "%s <%s> (%s)" % (self.name, self.email if self.email else u'sin email', self.address)

    def delivery_method_name(self):
        return self.prefered_delivery_method.name