# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0013_auto_20150314_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='landing_page',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
