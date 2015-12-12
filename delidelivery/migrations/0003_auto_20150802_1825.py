# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delidelivery', '0002_auto_20150802_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverymethod',
            name='delivery_day',
            field=models.IntegerField(null=True, verbose_name='día de entrega', choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='delivery_time',
            field=models.CharField(blank=True, verbose_name='hora de entrega', max_length=50),
            preserve_default=True,
        ),
    ]
