from django.db import models
from django.utils.translation import ugettext_lazy as _
from delidelivery.models import DeliveryMethod


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('nombre'))
    last_name = models.CharField(max_length=100, verbose_name=_('apellido'), blank=True)
    email = models.EmailField(verbose_name=_('e-mail'), blank=True)
    address = models.TextField(blank=True, verbose_name=_('dirección'))
    phone = models.CharField(max_length=200, blank=True,
        verbose_name=_('teléfono'))

    class Meta:
        verbose_name = _('persona')
        verbose_name_plural = _('personas')

    def __str__(self):
        return "%s %s" % (self.first_name)


class Customer(Person):
    prefered_delivery_method = models.ForeignKey(DeliveryMethod,
        verbose_name=_('método de envio preferido'))

    class Meta:
        verbose_name = _('cliente')
        verbose_name_plural = _('clientes')

    def __str__(self):
        return "%s %s" % (self.first_name)

    def delivery_method_name(self):
        return self.prefered_delivery_method.name