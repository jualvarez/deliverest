# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0023_order_delivery_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='comments',
            new_name='user_comments',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_price',
            field=models.DecimalField(decimal_places=4, default=0.0, help_text='Se completar\xe1 autom\xe1ticamente con la informaci\xf3n del env\xedo', max_digits=20, verbose_name='precio de env\xedo'),
        ),
    ]