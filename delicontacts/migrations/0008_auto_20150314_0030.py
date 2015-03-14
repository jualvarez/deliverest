# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0007_auto_20150219_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('name',), 'verbose_name': 'persona', 'verbose_name_plural': 'personas'},
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='nombre'),
            preserve_default=False,
        ),
    ]
