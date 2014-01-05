# -*- coding: utf-8 -*-
import autocomplete_light
from apps.cmp.models import Contract
from apps.cmp.models import Developer

# This will generate a PersonAutocomplete class
autocomplete_light.register(Contract,
    search_fields=['^num'],
    input_attrs={
        'placeholder': 'Начните печатать',
        'data-autocomplete-minimum-characters': 2,
    },
    attrs={
        'data-widget-minimum-characters': 1,
    },
)

autocomplete_light.register(Developer,
    search_fields=['^name'],
    input_attrs={
        'placeholder': 'Начните печатать',
        'data-autocomplete-minimum-characters': 2,
    },
    attrs={
        'data-widget-minimum-characters': 1,
    },
)
