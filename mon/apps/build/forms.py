# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building


class BuildForm(forms.ModelForm):
    address = forms.CharField(label=_('Address'), widget=forms.Textarea(attrs={'rows': 4, 'class': 'span6'}))

    class Meta:
        model = Building

    def __init__(self, *args, **kwargs):
        super(BuildForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'span7'

