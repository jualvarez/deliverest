# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

DELIVERY_DAY_CHOICES = (
        (0, _(u'Lunes')),
        (1, _(u'Martes')),
        (2, _(u'Miércoles')),
        (3, _(u'Jueves')),
        (4, _(u'Viernes')),
        (5, _(u'Sábado')),
        (6, _(u'Domingo')),
    )



class DeliveryMethod(models.Model):
    code = models.CharField(max_length=50, unique=True,
        verbose_name=_(u'código'))
    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))
    is_delivery = models.BooleanField(default=False, verbose_name=_(u'se entrega a domicilio'))
    pickup_address = models.TextField(verbose_name=_(u'dirección de recogida'), blank=True)
    delivery_day = models.IntegerField(verbose_name=_(u'día de entrega'), choices=DELIVERY_DAY_CHOICES)
    delivery_time = models.CharField(max_length=50, verbose_name=_(u'hora de entrega'), blank=True)

    class Meta:
        verbose_name = _(u'método de envío')
        verbose_name_plural = _(u'métodos de envío')

    def __unicode__(self):
        return unicode(self.name)