# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0006_auto_20141018_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='price',
        ),
        migrations.AddField(
            model_name='price',
            name='buy_price',
            field=models.DecimalField(decimal_places=4, verbose_name='precio de compra', default=0, max_digits=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, verbose_name='precio de venta', default=0, max_digits=20),
            preserve_default=False,
        ),
    ]
