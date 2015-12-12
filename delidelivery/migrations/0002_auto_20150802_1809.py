# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delidelivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverymethod',
            name='is_delivery',
            field=models.BooleanField(default=False, verbose_name='se entrega a domicilio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='pickup_address',
            field=models.TextField(verbose_name='dirección de recogida', blank=True),
            preserve_default=True,
        ),
    ]
