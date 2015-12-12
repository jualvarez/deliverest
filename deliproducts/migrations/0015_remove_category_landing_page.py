# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0014_category_landing_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='landing_page',
        ),
    ]
