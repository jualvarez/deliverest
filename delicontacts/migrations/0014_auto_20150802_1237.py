# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0013_auto_20150802_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_confirmed_tf',
            field=models.DateField(verbose_name='última confirmación de ventana de entrega', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='associated_user',
            field=models.ForeignKey(blank=True, null=True, verbose_name='usuario vinculado', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_mode',
            field=models.IntegerField(default=100, verbose_name='forma de contacto', choices=[(50, 'Web'), (100, 'E-mail'), (200, 'Facebook'), (300, 'Telefono'), (400, 'Otro')]),
            preserve_default=True,
        ),
    ]
