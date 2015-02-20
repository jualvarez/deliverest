# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0007_auto_20150219_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact_mode',
            field=models.IntegerField(blank=True, verbose_name='Forma de contacto', default=100, choices=[(100, 'E-mail'), (200, 'Facebook'), (300, 'Telefono'), (400, 'Otro')]),
            preserve_default=False,
        ),
    ]
