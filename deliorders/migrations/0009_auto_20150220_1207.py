# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0008_order_contact_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contact_mode',
            field=models.IntegerField(blank=True, choices=[(100, 'E-mail'), (200, 'Facebook'), (300, 'Telefono'), (400, 'Otro')], verbose_name='forma de contacto'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.date(2015, 2, 20), verbose_name='fecha de entrega'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=100, choices=[(100, 'Abierto'), (200, 'Cerrado'), (300, 'Entregado'), (400, 'Pagado pero no entregado'), (500, 'Entregado pero no pagado'), (600, 'Conciliado')], verbose_name='estado'),
            preserve_default=True,
        )
    ]
