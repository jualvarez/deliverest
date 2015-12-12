# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0011_auto_20150710_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='prefered_delivery_method',
            field=models.ForeignKey(null=True, verbose_name='método de envio preferido', to='delidelivery.DeliveryMethod'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.TextField(blank=True, verbose_name='dirección de envío'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='e-mail'),
            preserve_default=True,
        ),
    ]
