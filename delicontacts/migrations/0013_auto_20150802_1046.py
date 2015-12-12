# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0012_auto_20150801_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='prefered_delivery_method',
            field=models.ForeignKey(verbose_name='método de envio preferido', to='delidelivery.DeliveryMethod'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.TextField(verbose_name='dirección de envío'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(verbose_name='teléfono', max_length=200),
            preserve_default=True,
        ),
    ]
