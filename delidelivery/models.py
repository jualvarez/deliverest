# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeliveryMethod(models.Model):
    code = models.CharField(max_length=50, unique=True,
        verbose_name=_(u'código'))
    name = models.CharField(max_length=150, verbose_name=_(u'nombre'))

    class Meta:
        verbose_name = _(u'método de envío')
        verbose_name_plural = _(u'métodos de envío')

    def __str__(self):
        return self.name