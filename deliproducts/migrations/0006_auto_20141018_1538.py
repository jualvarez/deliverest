# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0005_auto_20141018_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='address',
            field=models.TextField(verbose_name='dirección', blank=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(max_length=100, verbose_name='teléfono', blank=True),
        ),
    ]
