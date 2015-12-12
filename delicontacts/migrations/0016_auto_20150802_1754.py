# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0015_auto_20150802_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='associated_user',
            field=models.OneToOneField(null=True, blank=True, verbose_name='usuario vinculado', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='prefered_delivery_method',
            field=models.ForeignKey(verbose_name='forma de envío preferida', to='delidelivery.DeliveryMethod'),
            preserve_default=True,
        ),
    ]
