# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(unique=True, max_length=50, verbose_name='código')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
            ],
            options={
                'verbose_name': 'método de envío',
                'verbose_name_plural': 'métodos de envío',
            },
            bases=(models.Model,),
        ),
    ]
