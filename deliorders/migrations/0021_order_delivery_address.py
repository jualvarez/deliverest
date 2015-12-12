# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0020_auto_20150802_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(default='Invalid delivery address', verbose_name='dirección de envío'),
            preserve_default=False,
        ),
    ]
