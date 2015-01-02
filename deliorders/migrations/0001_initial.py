# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0007_auto_20141019_0056'),
        ('delicontacts', '0005_auto_20141019_0056'),
        ('delidelivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(unique=True, max_length=50, verbose_name='código')),
                ('comments', models.TextField(verbose_name='notas')),
                ('when_create', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(verbose_name='cliente', to='delicontacts.Customer')),
                ('delivery_method', models.ForeignKey(to='delidelivery.DeliveryMethod')),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sell_price', models.DecimalField(decimal_places=4, verbose_name='precio de venta (si difiere)', null=True, max_digits=20)),
                ('quantity', models.IntegerField(verbose_name='cantidad')),
                ('comments', models.CharField(max_length=200, verbose_name='Notas')),
                ('order', models.ForeignKey(to='deliorders.Order')),
                ('product', models.ForeignKey(verbose_name='producto', to='deliproducts.Price')),
            ],
            options={
                'verbose_name': 'ítem de pedido',
                'verbose_name_plural': 'ítems de pedido',
            },
            bases=(models.Model,),
        ),
    ]
