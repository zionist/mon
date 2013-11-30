# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from .models import MO, RegionalBudget, FederalBudget, Subvention, DepartamentAgreement, PeopleAmount


class MOForm(forms.ModelForm):
    class Meta:
        model = MO
        fields = ('name', 'creation_form',)


class RegionalBudgetForm(forms.ModelForm):
    class Meta:
        model = RegionalBudget


class FederalBudgetForm(forms.ModelForm):
    class Meta:
        model = FederalBudget


class SubventionForm(forms.ModelForm):
    class Meta:
        model = Subvention


class DepartamentAgreementForm(forms.ModelForm):
    class Meta:
        model = DepartamentAgreement
        exclude = ('mo', )


class PeopleAmountForm(forms.ModelForm):
    class Meta:
        model = PeopleAmount


class MOShowForm(forms.ModelForm):
    class Meta:
        model = MO
        fields = ('name', 'creation_form',)

    def __init__(self, *args, **kwargs):
        super(MOShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class DepartamentAgreementShowForm(forms.ModelForm):
    class Meta:
        model = DepartamentAgreement
        exclude = ('mo', )

    def __init__(self, *args, **kwargs):
        super(DepartamentAgreementShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

