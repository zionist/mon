# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from .models import MO, RegionalBudget, FederalBudget, Subvention, DepartamentAgreement, PeopleAmount, MaxFlatPrice
from apps.core.models import CREATION_FORM_CHOICES
from apps.core.forms import CSIMultipleChoiceField, CSICheckboxSelectMultiple


class MOForm(forms.ModelForm):

    creation_form = CSIMultipleChoiceField(label=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
        required=False, widget=CSICheckboxSelectMultiple, choices=CREATION_FORM_CHOICES)

    class Meta:
        model = MO
        fields = ('name', 'creation_form', 'has_trouble', 'planing_home_orphans')


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


class MaxFlatPriceForm(forms.ModelForm):
    class Meta:
        model = MaxFlatPrice


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

    def __init__(self, *args, **kwargs):
        self.prev_mo = kwargs.get('initial').get('prev_mo') if 'initial' in kwargs else None
        super(DepartamentAgreementForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(DepartamentAgreementForm, self).clean()
        date = cd.get('date')
        if date and self.prev_mo and DepartamentAgreement.objects.filter(mo=self.prev_mo, date__gt=date, agreement_type=0).exists():
            msg = _(u'Неверная дата, уже есть соглашение с министерством с более поздней датой')
            self._errors["date"] = self.error_class([msg])
            del cd["date"]
        return cd


class PeopleAmountForm(forms.ModelForm):
    class Meta:
        model = PeopleAmount


class MOShowForm(forms.ModelForm):
    creation_form = CSIMultipleChoiceField(label=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
        required=False, widget=CSICheckboxSelectMultiple, choices=CREATION_FORM_CHOICES)

    class Meta:
        model = MO
        fields = ('name', 'creation_form',)

    def __init__(self, *args, **kwargs):
        super(MOShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class DepartamentAgreementShowForm(forms.ModelForm):
    class Meta:
        model = DepartamentAgreement
        exclude = ('mo', 'subvention')

    def __init__(self, *args, **kwargs):
        super(DepartamentAgreementShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class SubventionShowForm(forms.ModelForm):
    class Meta:
        model = Subvention
        exclude = ('date', 'reg_budget', 'fed_budget')

    def __init__(self, *args, **kwargs):
        super(SubventionShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class FederalBudgetShowForm(forms.ModelForm):
    class Meta:
        model = FederalBudget

    def __init__(self, *args, **kwargs):
        super(FederalBudgetShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class RegionalBudgetShowForm(forms.ModelForm):
    class Meta:
        model = RegionalBudget

    def __init__(self, *args, **kwargs):
        super(RegionalBudgetShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class MOPerformanceForm(forms.ModelForm):
    class Meta:
        model = MO
        fields = ('name', 'home_orphans')
