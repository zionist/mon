# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building, Ground
from apps.core.models import INTERNAL_DOORS_CHOICES, ENTRANCE_DOOR_CHOICES, WINDOW_CONSTRUCTIONS_CHOICES


class GroundForm(forms.ModelForm):
    internal_doors = forms.ChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
        widget=forms.Select, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = forms.ChoiceField(label=_(u"Материал входной двери"), required=False,
        widget=forms.Select, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = forms.ChoiceField(label=_(u"Материал оконных конструкций"), required=False,
        widget=forms.Select, choices=WINDOW_CONSTRUCTIONS_CHOICES)

    class Meta:
        model = Ground


class BuildingForm(GroundForm):
    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4 }))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), required=False, widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)


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
            for field in self.fields:
                if hasattr(self.instance, field):
                    if not hasattr(cmp_initial, field):
                        #self.fields[field].widget.attrs['hidden'] = 'hidden'
                        self.fields.pop(field)
                    elif hasattr(cmp_initial, field):
                        if getattr(self.instance, field) != getattr(cmp_initial, field):
                            self.fields[field].widget.attrs['style'] = 'background-color: red;'


class GroundShowForm(BuildingShowForm):

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract',
                   'address', 'comment', 'complete_date', 'readiness', 'payment_perspective')