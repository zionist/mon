# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment


class PaymentShowForm(forms.ModelForm):
    class Meta:
        model = Payment

    def __init__(self, *args, **kwargs):
        super(PaymentShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class DateForm(forms.Form):
    prev = forms.DateField(label=_(u'Начиная с'))
    dt = forms.DateField(label=_(u'по'))

