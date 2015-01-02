# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0002_auto_20141018_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='person',
            field=models.OneToOneField(to='delicontacts.Person', verbose_name='persona', null=True),
        ),
    ]
