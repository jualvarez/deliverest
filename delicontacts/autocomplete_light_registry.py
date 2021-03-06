# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from delicontacts.models import Customer

# This will generate a PersonAutocomplete class
autocomplete_light.registry.register(Customer,
    # Just like in ModelAdmin.search_fields
    search_fields=['name','address'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': _(u'Nombre de cliente'),
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 2,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 10,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)