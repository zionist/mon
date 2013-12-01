# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import CompareData, Contract, Result, Auction, Person


class CompareDataForm(forms.ModelForm):
    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen')


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ('cmp_data',)


class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person


class AuctionShowForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(AuctionShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class ContractShowForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(ContractShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class CompareDataShowForm(forms.ModelForm):
    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(CompareDataShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class ResultShowForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ('cmp_data',)

    def __init__(self, *args, **kwargs):
        super(ResultShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'



