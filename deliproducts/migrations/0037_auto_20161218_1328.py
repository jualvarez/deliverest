# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-18 16:28
from __future__ import unicode_literals

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0036_auto_20161218_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=markdownx.models.MarkdownxField(blank=True, help_text='descripci\xf3n que se muestra en el detalle de producto', verbose_name='descripci\xf3n larga'),
        ),
    ]
