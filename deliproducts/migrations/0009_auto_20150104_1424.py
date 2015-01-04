# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0008_auto_20150104_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='wholesale',
        ),
        migrations.AddField(
            model_name='price',
            name='wholesale',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
