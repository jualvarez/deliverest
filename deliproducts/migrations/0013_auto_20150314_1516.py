# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0012_auto_20150104_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='nombre', unique=True, max_length=150)),
                ('color', models.CharField(null=True, help_text='color de identificación de la categoría', max_length=8, blank=True, verbose_name='color')),
                ('children_color', models.CharField(null=True, help_text='color de identificación para los hijos de esta categoría', max_length=8, blank=True, verbose_name='color de los hijos')),
                ('parent', models.ForeignKey(null=True, related_name='category', to='deliproducts.Category', verbose_name='categoría padre', blank=True)),
            ],
            options={
                'verbose_name': 'categoría',
                'verbose_name_plural': 'categorías',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, to='deliproducts.Category', verbose_name='categoría', blank=True),
            preserve_default=True,
        ),
    ]
