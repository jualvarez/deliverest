# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0021_order_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, verbose_name='fecha de entrega'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(to='delidelivery.DeliveryMethod', default=1, verbose_name='método de envío', blank=True),
            preserve_default=False,
        ),
    ]
