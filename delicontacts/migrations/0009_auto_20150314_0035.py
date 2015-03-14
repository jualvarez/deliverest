# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def copy_names(apps, schema_editor):
	Person = apps.get_model('delicontacts', 'Person')
	for person in Person.objects.all():
		person.name = person.first_name
		person.save()

def copy_first_names(apps, schema_editor):
	Person = apps.get_model('delicontacts', 'Person')
	for person in Person.objects.all():
		person.fisrt_name = person.name
		person.save()

class Migration(migrations.Migration):

    dependencies = [
        ('delicontacts', '0008_auto_20150314_0030'),
    ]

    operations = [
    	migrations.RunPython(copy_names, copy_first_names)
    ]
