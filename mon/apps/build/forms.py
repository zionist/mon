# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building, Ground
from apps.core.models import INTERNAL_DOORS_CHOICES, ENTRANCE_DOOR_CHOICES, WINDOW_CONSTRUCTIONS_CHOICES, \
    STATE_CHOICES, WATER_SETTLEMENT_CHOICES, HOT_WATER_SUPPLY_CHOICES, Developer
from apps.core.forms import cmp_single


class GroundForm(forms.ModelForm):
    internal_doors = forms.ChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
        widget=forms.Select, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = forms.ChoiceField(label=_(u"Материал входной двери"), required=False,
        widget=forms.Select, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = forms.ChoiceField(label=_(u"Материал оконных конструкций"), required=False,
        widget=forms.Select, choices=WINDOW_CONSTRUCTIONS_CHOICES)
    water_settlement = forms.ChoiceField(label=_(u"Водоподведение"), required=False,
        widget=forms.Select, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = forms.ChoiceField(label=_(u"Горячее водоснабжение"), required=False,
        widget=forms.Select, choices=HOT_WATER_SUPPLY_CHOICES)

    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4 }))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), required=False, widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'developer', 'state')


class BuildingForm(GroundForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'developer', 'state')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)


class BuildingSelectForm(forms.Form):
    state = forms.ChoiceField(label=_(u'Тип объекта'), required=True, choices=STATE_CHOICES, help_text=_(u"Тип объекта"), )
    developer = forms.ModelChoiceField(label=_(u'Выберите застройщика (будет предложено добавить нового при пустом значении)'),
        required=False, queryset=Developer.objects.all(),
        help_text=_(u"Выберите застройщика (будет предложено добавить нового при пустом значении)"), )

class BuildingShowForm(BuildingForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract',
                   'address', 'comment', 'complete_date', 'readiness', 'payment_perspective')

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(BuildingShowForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget')and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

        if cmp_initial:
            cmp_single(self, cmp_initial)


class GroundShowForm(BuildingShowForm):

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract',
                   'address', 'comment', 'complete_date', 'readiness', 'payment_perspective')
