# -*- coding: utf-8 -*-
import autocomplete_light
from apps.build.models import Building
from apps.build.models import Ground

autocomplete_light.register(Building,
    search_fields=['^address'],
    input_attrs={
        'placeholder': 'Начните печатать',
        'data-autocomplete-minimum-characters': 2,
    },
    attrs={
        'data-widget-minimum-characters': 1,
    },
)

autocomplete_light.register(Ground,
    search_fields=['^address'],
    input_attrs={
        'placeholder': 'Начните печатать',
        'data-autocomplete-minimum-characters': 2,
    },
    attrs={
        'data-widget-minimum-characters': 1,
    },
)
