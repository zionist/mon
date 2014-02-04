# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from .models import MO, RegionalBudget, FederalBudget, Subvention, DepartamentAgreement, PeopleAmount
from apps.core.models import CREATION_FORM_CHOICES
from apps.core.forms import CSIMultipleChoiceField, CSICheckboxSelectMultiple


class MOForm(forms.ModelForm):

    creation_form = CSIMultipleChoiceField(label=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
        required=False, widget=CSICheckboxSelectMultiple, choices=CREATION_FORM_CHOICES)

    class Meta:
        model = MO
        fields = ('name', 'creation_form', 'has_trouble')


class RegionalBudgetForm(forms.ModelForm):
    class Meta:
        model = RegionalBudget


class FederalBudgetForm(forms.ModelForm):
    class Meta:
        model = FederalBudget


class SubventionForm(forms.ModelForm):
    class Meta:
        model = Subvention
        exclude = ('date', 'reg_budget', 'fed_budget')


class SubventionMinusForm(forms.ModelForm):

    class Meta:
        model = Subvention
        exclude = ('date', 'reg_budget', 'fed_budget')

    def __init__(self, *args, **kwargs):
        super(SubventionMinusForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = _(u'Сумма субвенции, подлежащая вычету')

    def clean(self):
        cd = super(SubventionMinusForm, self).clean()
        amount = cd.get('amount')
        if amount and int(amount) > 0:
            msg = _(u'Должно быть отрицательным')
            self._errors["amount"] = self.error_class([msg])
            del cd["amount"]
        return cd


class DepartamentAgreementForm(forms.ModelForm):
    class Meta:
        model = DepartamentAgreement
        exclude = ('mo', 'subvention', 'agreement_type')

#    def __init__(self, mo=None, *args, **kwargs):
#        self.prev_mo = kwargs.pop('prev_mo') if 'prev_mo' in kwargs else None
#        super(DepartamentAgreementForm, self).__init__(*args, **kwargs)

#    def clean(self):
#        cd = super(DepartamentAgreementForm, self).clean()
#        date = cd.get('date')
#        if date and self.mo and DepartamentAgreement.objects.filter(mo=self.prev_mo, date__gt=date).exists():
#            msg = _(u'Неверная дата')
#            self._errors["date"] = self.error_class([msg])
#            del cd["date"]
#        return cd



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
        exclude = ('mo', 'subvention')

    def __init__(self, *args, **kwargs):
        super(DepartamentAgreementShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class SubventionShowForm(forms.ModelForm):
    class Meta:
        model = Subvention
        exclude = ('date', 'reg_budget', 'fed_budget')

    def __init__(self, *args, **kwargs):
        super(SubventionShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class FederalBudgetShowForm(forms.ModelForm):
    class Meta:
        model = FederalBudget

    def __init__(self, *args, **kwargs):
        super(FederalBudgetShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class RegionalBudgetShowForm(forms.ModelForm):
    class Meta:
        model = RegionalBudget

    def __init__(self, *args, **kwargs):
        super(RegionalBudgetShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class MOPerformanceForm(forms.ModelForm):
    class Meta:
        model = MO
        fields = ('name', 'home_orphans')
