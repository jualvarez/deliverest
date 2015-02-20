# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0006_auto_20150104_1253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'persona', 'verbose_name_plural': 'personas', 'ordering': ('first_name', 'last_name')},
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_mode',
            field=models.IntegerField(verbose_name='Forma de contacto', default=100, choices=[(100, 'E-mail'), (200, 'Facebook'), (300, 'Telefono'), (400, 'Otro')]),
            preserve_default=True,
        ),
    ]
