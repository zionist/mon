# -*- coding: utf-8 -*-
import autocomplete_light
from apps.mo.models import MO

# This will generate a PersonAutocomplete class
autocomplete_light.register(MO,
    search_fields=['^name'],
    input_attrs={
        'placeholder': 'Начните печатать',
        'data-autocomplete-minimum-characters': 2,
    },
    attrs={
        'data-widget-minimum-characters': 1,
    },
)
