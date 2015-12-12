# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0014_auto_20150802_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='associated_user',
            field=models.OneToOneField(verbose_name='usuario vinculado', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
