# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0003_auto_20141026_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='reconciled',
            field=models.BooleanField(verbose_name='conciliado', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='fecha de entrega', default=datetime.date(2014, 11, 1)),
        ),
    ]
