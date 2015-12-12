# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0018_auto_20150707_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='plural_name',
            field=models.CharField(null=True, verbose_name='plural', max_length=150),
            preserve_default=True,
        ),
    ]
