# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0016_auto_20150802_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail'),
        ),
    ]