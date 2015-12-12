# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

def add_category_slug(apps, schema_editor):
	Category = apps.get_model("deliproducts", "Category")
	for cat in Category.objects.all():
		cat.slug = slugify(cat.name)
		cat.save()

class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0017_category_slug'),
    ]

    operations = [
    	migrations.RunPython(add_category_slug)
    ]
