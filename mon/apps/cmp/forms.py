# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from django.forms import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from .models import CompareData, Contract, Result, Auction, Person
from apps.core.models import INTERNAL_DOORS_CHOICES, ENTRANCE_DOOR_CHOICES, WINDOW_CONSTRUCTIONS_CHOICES


class CSICheckboxSelectMultiple(CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        if value:
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(name, value, attrs=attrs, choices=choices)


class CSIMultipleChoiceField(MultipleChoiceField):
    widget = CSICheckboxSelectMultiple

    def to_python(self, value):
        return value

    def validate(self, value):
        if value:
            value = value.split(',')
        super(CSIMultipleChoiceField, self).validate(value)
        return


class CompareDataForm(forms.ModelForm):
    internal_doors = forms.ChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
        widget=forms.Select, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = forms.ChoiceField(label=_(u"Материал входной двери"), required=False,
        widget=forms.Select, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = forms.ChoiceField(label=_(u"Материал оконных конструкций"), required=False,
        widget=forms.Select, choices=WINDOW_CONSTRUCTIONS_CHOICES)
    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')
#        fields = ('cmp_date', )


class ContractForm(forms.ModelForm):
    internal_doors = forms.ChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
        widget=forms.Select, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = forms.ChoiceField(label=_(u"Материал входной двери"), required=False,
        widget=forms.Select, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = forms.ChoiceField(label=_(u"Материал оконных конструкций"), required=False,
        widget=forms.Select, choices=WINDOW_CONSTRUCTIONS_CHOICES)
    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen')


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result
        exclude = ('cmp_data', )
    recommend = forms.CharField(help_text=_(u"Рекомендации"), label=_(u'Рекомендации'), widget=forms.Textarea(attrs={'rows': 4 }))


class AuctionForm(forms.ModelForm):
    internal_doors = CSIMultipleChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
        widget=CSICheckboxSelectMultiple, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = CSIMultipleChoiceField(label=_(u"Материал входной двери"), required=False,
        widget=CSICheckboxSelectMultiple, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = CSIMultipleChoiceField(label=_(u"Материал оконных конструкций"), required=False,
        widget=CSICheckboxSelectMultiple, choices=WINDOW_CONSTRUCTIONS_CHOICES)

    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen')


class PersonForm(forms.ModelForm):
    position = forms.CharField(help_text=_(u"Должность"), label=_(u'Должность'), required=False,
                               widget=forms.Textarea(attrs={'rows': 2}))

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
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'num', 'name', 'summa', 'sign_date')

    def __init__(self, *args, **kwargs):

        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(ContractShowForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

        if cmp_initial:
            for field in self.fields:
                if hasattr(self.instance, field) and hasattr(cmp_initial, field):
                    if getattr(self.instance, field) != getattr(cmp_initial, field):
                        self.fields[field].widget.attrs['style'] = 'background-color: red;'


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
        exclude = ('cmp_data', )

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(ResultShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

        if cmp_initial:
            for field in self.fields:
                if hasattr(self.instance, field) and hasattr(cmp_initial, field):
                    if getattr(self.instance, field) != getattr(cmp_initial, field):
                        self.fields[field].widget.attrs['style'] = 'background-color: red;'
