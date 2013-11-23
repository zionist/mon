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

class PeopleAmountForm(forms.ModelForm):
    class Meta:
        model = PeopleAmount
