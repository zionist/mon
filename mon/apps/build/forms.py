# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building, Ground


class GroundForm(forms.ModelForm):
    class Meta:
        model = Ground


class BuildingForm(forms.ModelForm):
    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4 }))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), required=False, widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)

    def to_table(self):
        return "<td> %s </td> <td> %s </td> <td> %s </td>" % (self.address, self.mo.name, self.developer)

class BuildingShowForm(BuildingForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(BuildingShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
