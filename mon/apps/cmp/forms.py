# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet


from .models import CompareData, Result, Auction, Person, AuctionDocuments
from apps.build.models import Contract, ContractDocuments
from apps.core.models import INTERNAL_DOORS_CHOICES, ENTRANCE_DOOR_CHOICES, WINDOW_CONSTRUCTIONS_CHOICES, \
    WATER_SETTLEMENT_CHOICES, HOT_WATER_SUPPLY_CHOICES
from apps.core.forms import CSIMultipleChoiceField, CSICheckboxSelectMultiple


class CompareDataForm(forms.ModelForm):

    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')
#        fields = ('cmp_date', )


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'docs')


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result
        exclude = ('cmp_data', )
    recommend = forms.CharField(help_text=_(u"Рекомендации"), label=_(u'Рекомендации'), widget=forms.Textarea(attrs={'rows': 4 }))


class AuctionDocumentsForm(forms.ModelForm):

    class Meta:
        model = AuctionDocuments


class ContractDocumentsForm(forms.ModelForm):

    class Meta:
        model = ContractDocuments


class AuctionForm(forms.ModelForm):
    internal_doors = CSIMultipleChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
                                            widget=CSICheckboxSelectMultiple, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = CSIMultipleChoiceField(label=_(u"Материал входной двери"), required=False,
                                           widget=CSICheckboxSelectMultiple, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = CSIMultipleChoiceField(label=_(u"Материал оконных конструкций"), required=False,
                                                  widget=CSICheckboxSelectMultiple, choices=WINDOW_CONSTRUCTIONS_CHOICES)
    water_settlement = CSIMultipleChoiceField(label=_(u"Водоподведение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = CSIMultipleChoiceField(label=_(u"Горячее водоснабжение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=HOT_WATER_SUPPLY_CHOICES)

    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'docs')


class PersonForm(forms.ModelForm):
    position = forms.CharField(help_text=_(u"Должность"), label=_(u'Должность'), required=False,
                               widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Person


class AuctionShowForm(forms.ModelForm):
    internal_doors = CSIMultipleChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
                                            widget=CSICheckboxSelectMultiple, choices=INTERNAL_DOORS_CHOICES)
    entrance_door = CSIMultipleChoiceField(label=_(u"Материал входной двери"), required=False,
                                           widget=CSICheckboxSelectMultiple, choices=ENTRANCE_DOOR_CHOICES)
    window_constructions = CSIMultipleChoiceField(label=_(u"Материал оконных конструкций"), required=False,
                                                  widget=CSICheckboxSelectMultiple, choices=WINDOW_CONSTRUCTIONS_CHOICES)
    water_settlement = CSIMultipleChoiceField(label=_(u"Водоподведение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = CSIMultipleChoiceField(label=_(u"Горячее водоснабжение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=HOT_WATER_SUPPLY_CHOICES)

    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'docs')

    def __init__(self, *args, **kwargs):
        super(AuctionShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class ContractShowForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'num', 'name', 'summa', 'sign_date', 'docs')

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
