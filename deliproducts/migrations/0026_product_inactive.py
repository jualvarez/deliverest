# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0025_auto_20160120_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inactive',
            field=models.BooleanField(default=False, verbose_name='desactivar'),
        ),
    ]