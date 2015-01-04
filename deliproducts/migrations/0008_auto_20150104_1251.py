# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0007_auto_20141019_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='quantifiable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='presentation',
            name='measure_unit',
            field=models.CharField(blank=True, max_length=2, choices=[('L', 'litro'), ('CC', 'cc'), ('G', 'gramo'), ('KG', 'kilogramo'), ('U', 'unidad')], null=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='quantity',
            field=models.DecimalField(max_digits=6, verbose_name='cantidad', blank=True, decimal_places=2, null=True),
        ),
    ]
