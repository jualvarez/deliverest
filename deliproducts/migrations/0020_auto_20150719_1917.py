# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def pluralize_presentation_name(apps, schema_editor):
	Presentation = apps.get_model("deliproducts", "Presentation")
	for pres in Presentation.objects.all():
		pres.plural_name = pres.name + "s"
		pres.save()

class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0019_presentation_plural_name'),
    ]

    operations = [
    	migrations.RunPython(pluralize_presentation_name)
    ]
