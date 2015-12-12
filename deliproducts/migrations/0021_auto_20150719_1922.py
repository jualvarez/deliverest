# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0020_auto_20150719_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='plural_name',
            field=models.CharField(verbose_name='plural', max_length=150, default='Failed to pluralize'),
            preserve_default=False,
        ),
    ]
