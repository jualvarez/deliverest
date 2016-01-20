from django.db import models
from django.utils.translation import ugettext_lazy as _


class PromoImage(models.Model):
	image = models.ImageField(upload_to='promo-images', verbose_name=_(u'imágen'), width_field='width', height_field='height')
	width = models.FloatField(blank=True, null=True)
	height = models.FloatField(blank=True, null=True)
	description = models.CharField(verbose_name=_(u'descripción'), max_length=150)
	is_active = models.BooleanField(default=True, verbose_name=_(u'activa'))

	class Meta:
		verbose_name = _(u'imágen de promoción')
		verbose_name_plural = _(u'imágenes de promoción')