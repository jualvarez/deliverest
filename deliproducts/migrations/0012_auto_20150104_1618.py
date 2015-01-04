# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0011_auto_20150104_1604'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=set([('product', 'presentation', 'wholesale')]),
        ),
    ]
