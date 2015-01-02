# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0003_auto_20141018_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(null=True, to='deliproducts.Provider'),
        ),
    ]
