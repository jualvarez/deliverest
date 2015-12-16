# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0022_price_in_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ('sell_price',), 'verbose_name_plural': 'precios', 'verbose_name': 'precio'},
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nombre'),
            preserve_default=True,
        ),
    ]
