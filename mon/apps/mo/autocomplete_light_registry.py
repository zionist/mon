# -*- coding: utf-8 -*-
import autocomplete_light
from apps.mo.models import MO

# This will generate a PersonAutocomplete class
autocomplete_light.register(MO,
    search_fields=['^name'],
    attrs={
        'placeholder': 'Начните печатать',
        'data-widget-minimum-characters': 1,
    },
)
