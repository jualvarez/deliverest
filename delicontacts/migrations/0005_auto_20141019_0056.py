# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delidelivery', '0001_initial'),
        ('delicontacts', '0004_auto_20141018_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='delivery_method',
        ),
        migrations.DeleteModel(
            name='DeliveryMethod',
        ),
        migrations.AddField(
            model_name='customer',
            name='prefered_delivery_method',
            field=models.ForeignKey(verbose_name='método de envio preferido', to='delidelivery.DeliveryMethod', default=1),
            preserve_default=False,
        ),
    ]
