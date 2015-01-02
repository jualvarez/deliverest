# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(verbose_name='código', max_length=50, unique=True)),
                ('name', models.CharField(verbose_name='nombre', max_length=150)),
            ],
            options={
                'verbose_name': 'método de envío',
                'verbose_name_plural': 'métodos de envío',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(verbose_name='nombre', max_length=100)),
                ('last_name', models.CharField(verbose_name='apellido', max_length=100)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=75)),
                ('address', models.TextField(verbose_name='dirección', blank=True)),
                ('phone', models.CharField(verbose_name='teléfono', blank=True, max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'persona',
                'verbose_name_plural': 'personas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='delivery_method',
            field=models.ForeignKey(verbose_name='método de envio', to='delicontacts.DeliveryMethod'),
            preserve_default=True,
        ),
    ]
