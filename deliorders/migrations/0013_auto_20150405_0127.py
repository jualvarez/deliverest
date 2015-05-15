# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0012_auto_20150329_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='fecha de entrega', default=datetime.date(2015, 4, 5)),
            preserve_default=True,
        ),
    ]
