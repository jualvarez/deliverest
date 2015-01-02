# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0003_auto_20141018_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='person',
        ),
        migrations.AddField(
            model_name='customer',
            name='person_ptr',
            field=models.OneToOneField(primary_key=True, parent_link=True, serialize=False, default=1, to='delicontacts.Person', auto_created=True),
            preserve_default=False,
        ),
    ]
