# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0010_auto_20150104_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='quantifiable',
            field=models.BooleanField(default=True, verbose_name='cuantificable'),
        ),
        migrations.AlterField(
            model_name='price',
            name='wholesale',
            field=models.BooleanField(default=False, verbose_name='Por mayor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(blank=True, to='deliproducts.Provider', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='presentation',
            unique_together=set([('name', 'quantity', 'measure_unit')]),
        ),
    ]
