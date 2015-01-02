# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='person',
            name='object_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='person',
            field=models.ForeignKey(verbose_name='persona', null=True, to='delicontacts.Person'),
            preserve_default=True,
        ),
    ]
