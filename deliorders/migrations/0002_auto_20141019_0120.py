# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(verbose_name='estado', default=100, choices=[(100, 'Abierto'), (200, 'Cerrado'), (300, 'Entregado'), (400, 'Pagado pero no entregado'), (500, 'Entregado pero no pagado')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='when_create',
            field=models.DateTimeField(verbose_name='fechas de pedido', auto_now_add=True),
        ),
    ]
