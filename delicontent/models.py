# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from markdownx.models import MarkdownxField


class Page(models.Model):
    slug = models.SlugField(verbose_name=u'slug')
    short_title = models.CharField(verbose_name=u'título corto', help_text=u'Este título se usa para mostrar en los links', max_length=50)
    title = models.CharField(verbose_name=u'título', max_length=200)
    content = MarkdownxField(verbose_name=_(u'contenido'), help_text=_(u'Contenido de la página'), blank=True)

    show_in_nav = models.BooleanField(verbose_name='mostrar en la navegación')
    order = models.PositiveIntegerField(verbose_name='orden para mostrar', default=0)

    class Meta:
        verbose_name = _(u'página')
        verbose_name_plural = _(u'páginas')

        ordering = ('order', 'title')


class PromoImage(models.Model):
    image = models.ImageField(upload_to='promo-images', verbose_name=_(u'imágen'), width_field='width', height_field='height')
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    description = models.CharField(verbose_name=_(u'descripción'), max_length=150)
    is_active = models.BooleanField(default=True, verbose_name=_(u'activa'))

    class Meta:
        verbose_name = _(u'imágen de promoción')
        verbose_name_plural = _(u'imágenes de promoción')
