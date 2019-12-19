# -*- coding: utf-8 -*-

from datetime import date

from constance import config
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from deliorders import utils

DELIVERY_DAY_CHOICES = (
    (0, _(u'Lunes')),
    (1, _(u'Martes')),
    (2, _(u'Miércoles')),
    (3, _(u'Jueves')),
    (4, _(u'Viernes')),
    (5, _(u'Sábado')),
    (6, _(u'Domingo')),
)


@python_2_unicode_compatible
class DeliveryMethod(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(u'código'))
    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))
    is_delivery = models.BooleanField(default=False, verbose_name=_(u'se entrega a domicilio'))
    pickup_address = models.TextField(verbose_name=_(u'dirección de recogida'), blank=True)
    notes = models.TextField(verbose_name=_(u'notas'), help_text=_('Este texto se muestra en el pie del e-mail de confirmacion'), blank=True)
    delivery_day = models.IntegerField(verbose_name=_(u'día de entrega'), choices=DELIVERY_DAY_CHOICES)
    delivery_time = models.CharField(max_length=50, verbose_name=_(u'hora de entrega'), blank=True)
    delivery_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=config.DELIVERY_DEFAULT_PRICE,
        verbose_name=_(u'precio de envío'))
    is_active = models.BooleanField(default=True, verbose_name=_(u'está activo'))

    class Meta:
        verbose_name = _(u'método de envío')
        verbose_name_plural = _(u'métodos de envío')

    def __str__(self):
        return self.name

    def next_delivery_date(self, dt=None):
        """ Calculates the next possible delivery date after datetime dt """
        if not dt:
            dt = timezone.now()

        return utils.next_open_day(dt, self.delivery_day)
