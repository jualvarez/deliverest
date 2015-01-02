# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0004_auto_20141018_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='deliproducts.Provider'),
        ),
    ]
