# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0009_auto_20150104_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='code',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(unique=True, verbose_name='nombre', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='deliproducts.Provider', null=True),
        ),
    ]
