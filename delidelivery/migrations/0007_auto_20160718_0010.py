# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-18 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delidelivery', '0006_deliverymethod_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverymethod',
            name='delivery_price',
            field=models.DecimalField(decimal_places=4, default=40.0, max_digits=20, verbose_name='precio de env\xedo'),
        ),
        migrations.AlterField(
            model_name='deliverymethod',
            name='notes',
            field=models.TextField(blank=True, help_text='Este texto se muestra en el pie del e-mail de confirmacion', verbose_name='notas'),
        ),
    ]
