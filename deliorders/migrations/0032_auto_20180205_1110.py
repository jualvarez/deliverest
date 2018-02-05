# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-02-05 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0031_auto_20170619_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='delicontacts.Customer', verbose_name='cliente'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='deliproducts.Price', verbose_name='producto'),
        ),
    ]
