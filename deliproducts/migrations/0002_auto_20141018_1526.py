# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(verbose_name='código', max_length=50)),
                ('name', models.CharField(verbose_name='nombre', max_length=150)),
                ('address', models.TextField(verbose_name='dirección')),
                ('phone', models.CharField(verbose_name='teléfono', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'proveedores',
                'verbose_name': 'proveedor',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(null=True, to='deliproducts.Provider'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(unique=True, verbose_name='codigo', max_length=50),
        ),
    ]
