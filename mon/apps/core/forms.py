# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Room, WC, Hallway, Kitchen


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room


class HallwayForm(forms.ModelForm):

    class Meta:
        model = Hallway


class WCForm(forms.ModelForm):

    class Meta:
        model = WC


class KitchenForm(forms.ModelForm):

    class Meta:
        model = Kitchen


class RoomShowForm(forms.ModelForm):

    class Meta:
        model = Room

    def __init__(self, *args, **kwargs):
        super(RoomShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class HallwayShowForm(forms.ModelForm):

    class Meta:
        model = Hallway

    def __init__(self, *args, **kwargs):
        super(HallwayShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class WCShowForm(forms.ModelForm):

    class Meta:
        model = WC

    def __init__(self, *args, **kwargs):
        super(WCShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class KitchenShowForm(forms.ModelForm):

    class Meta:
        model = Kitchen

    def __init__(self, *args, **kwargs):
        super(KitchenShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
