# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Payment
from apps.build.models import Contract
from apps.mo.models import Subvention


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('num', 'date', 'amount', 'contract', 'subvention', 'pay_order', 'approve_status')

    def __init__(self, *args, **kwargs):
        user_mo = kwargs.get('initial').get('user_mo') if 'initial' in kwargs else None
        super(PaymentForm, self).__init__(*args, **kwargs)
        if user_mo:
            self.fields['subvention'].queryset = Subvention.objects.filter(departamentagreement__mo=user_mo)
            self.fields['contract'].queryset = Contract.objects.filter(mo=user_mo)


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

