# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building, Ground
from apps.core.models import Room, WC, Hallway, Kitchen


class GroundForm(forms.ModelForm):
    class Meta:
        model = Ground


class BuildingForm(forms.ModelForm):
    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4, 'class': 'span6'}))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), widget=forms.Textarea(attrs={'rows': 4, 'class': 'span6'}))

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'span7'


class BuildingShowForm(BuildingForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(BuildingShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class RoomForm(BuildingForm):

    class Meta:
        model = Room


class WCForm(BuildingForm):

    class Meta:
        model = WC


class HallwayForm(BuildingForm):

    class Meta:
        model = Hallway


class KitchenForm(BuildingForm):

    class Meta:
        model = Kitchen