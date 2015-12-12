# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delicontacts', '0010_remove_person_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='associated_user',
            field=models.ForeignKey(null=True, verbose_name='Usuario vinculado', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_mode',
            field=models.IntegerField(default=100, choices=[(50, 'Web'), (100, 'E-mail'), (200, 'Facebook'), (300, 'Telefono'), (400, 'Otro')], verbose_name='Forma de contacto'),
            preserve_default=True,
        ),
    ]
