# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0002_auto_20141019_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.date(2014, 10, 26), verbose_name='fecha de entrega'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='when_closed',
            field=models.DateField(null=True, verbose_name='fecha de cierre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='when_delivered',
            field=models.DateField(null=True, verbose_name='fecha de entrega'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(verbose_name='notas', blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(verbose_name='método de envío', null=True, blank=True, to='delidelivery.DeliveryMethod'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=100, choices=[(100, 'Abierto'), (200, 'Cerrado'), (300, 'Entregado'), (400, 'Pagado pero no entregado'), (500, 'Entregado pero no pagado')], verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='order',
            name='when_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='fecha de pedido'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='comments',
            field=models.CharField(max_length=200, verbose_name='Notas', blank=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sell_price',
            field=models.DecimalField(max_digits=20, decimal_places=4, verbose_name='precio de venta (si difiere)', blank=True),
        ),
    ]
