# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-16 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delidelivery', '0007_auto_20160718_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverymethod',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='est\xe1 activo'),
        ),
    ]
