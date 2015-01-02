# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='nombre', max_length=150)),
                ('quantity', models.DecimalField(verbose_name='cantidad', max_digits=6, decimal_places=2)),
                ('measure_unit', models.CharField(choices=[('L', 'litro'), ('ML', 'mililitro'), ('G', 'gramo'), ('KG', 'kilogramo'), ('U', 'unidad')], max_length=2)),
            ],
            options={
                'verbose_name': 'presentación',
                'verbose_name_plural': 'presentaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('currency', models.CharField(verbose_name='moneda', default='ARS', max_length=3, choices=[('ARS', 'Peso argentino'), ('USD', 'Dolar')])),
                ('price', models.DecimalField(verbose_name='precio', max_digits=20, decimal_places=4)),
                ('presentation', models.ForeignKey(verbose_name='presentación', to='deliproducts.Presentation')),
            ],
            options={
                'verbose_name': 'precio',
                'verbose_name_plural': 'precios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(verbose_name='codigo', max_length=50)),
                ('name', models.CharField(verbose_name='nombre', max_length=200)),
                ('description', models.CharField(verbose_name='descripción', max_length=500)),
                ('presentations', models.ManyToManyField(to='deliproducts.Presentation', through='deliproducts.Price')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(verbose_name='producto', to='deliproducts.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=set([('product', 'presentation')]),
        ),
    ]
