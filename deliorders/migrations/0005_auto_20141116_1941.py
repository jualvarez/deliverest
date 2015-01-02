# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0004_auto_20141101_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(verbose_name='estado', default=100, choices=[(100, 'Abierto'), (200, 'Cerrado'), (300, 'Entregado'), (400, 'Pagado pero no entregado'), (500, 'Entregado pero no pagado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='fecha de entrega', default=datetime.date(2014, 11, 16)),
        ),
    ]
