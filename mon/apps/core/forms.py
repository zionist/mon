# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Room, WC, Hallway, Kitchen, Developer


class DeveloperForm(forms.ModelForm):
    boss_position = forms.CharField(help_text=_(u"Ф.И.О. и должность руководителя"), required=False,
                                    label=_(u'Ф.И.О. и должность руководителя'), widget=forms.Textarea(attrs={'rows': 4}))
    address = forms.CharField(help_text=_(u"Фактический адрес"), label=_(u'Фактический адрес'), required=False,
                              widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Developer
        exclude = ('doc', 'image')

    def __init__(self, *args, **kwargs):
        super(DeveloperForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') \
                and not hasattr(self.fields[field].widget.attrs, 'hidden') \
                and not isinstance(self.fields[field].widget, forms.Textarea):
                self.fields[field].widget.attrs['class'] = 'span5'
                self.fields[field].widget.attrs['style'] = 'height:26px;'


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

        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(RoomShowForm, self).__init__(*args, **kwargs)

        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class HallwayShowForm(forms.ModelForm):

    class Meta:
        model = Hallway

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(HallwayShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class WCShowForm(forms.ModelForm):

    class Meta:
        model = WC

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(WCShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class KitchenShowForm(forms.ModelForm):

    class Meta:
        model = Kitchen

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(KitchenShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'
