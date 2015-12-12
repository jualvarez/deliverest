# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0021_auto_20150719_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='in_stock',
            field=models.BooleanField(default=True, verbose_name='en stock'),
            preserve_default=True,
        ),
    ]
