from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeliveryMethod(models.Model):
    code = models.CharField(max_length=50, unique=True,
        verbose_name=_('código'))
    name = models.CharField(max_length=150, verbose_name=_('nombre'))

    class Meta:
        verbose_name = _('método de envío')
        verbose_name_plural = ('métodos de envío')

    def __str__(self):
        return self.name