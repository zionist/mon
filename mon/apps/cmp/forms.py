# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
import autocomplete_light


from .models import CompareData, Result, Auction, Person
from apps.build.models import Contract, ContractDocuments, Building
from apps.core.models import WATER_SETTLEMENT_CHOICES, HOT_WATER_SUPPLY_CHOICES, WATER_REMOVAL_CHOICES, \
    HEATING_CHOICES, ELECTRIC_SUPPLY_CHOICES
from apps.core.forms import CSIMultipleChoiceField, CSICheckboxSelectMultiple, cmp_single, cmp_multi
from apps.core.models import Choices
from apps.mo.models import MO


class CompareDataForm(forms.ModelForm):

    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')

        fields = [
            # ! no area and cmp_date in tech document
            'cmp_date',
            'area',
            'floors',
            'driveways',
            'electric_supply',
            'water_settlement',
            'water_removal',
            'hot_water_supply',
            'heating',
            'gas_supply',
            'internal_doors',
            'entrance_door',
            'window_constructions',
            'is_water_boiler',
            'is_loggia',
            'is_balcony',
            'kindergarden',
            'school',
            'clinic',
            'market',
            'public_transport',
            'is_routes',
            'is_playground',
            'is_clother_drying',
            'is_dustbin_area',
            'is_parking',

            # for remove or hide
            # 'is_heat_boiler',
            # 'is_intercom',
            # 'planing_floor',
            # 'floor',
            # 'flats_amount',
            # 'area_cmp',
        ]

    def __init__(self, *args, **kwargs):
        super(CompareDataForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = forms.ChoiceField(label=u"Материал межкомнатных дверей", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = forms.ChoiceField(label=u"Материал входной двери", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = forms.ChoiceField(label=u"Материал оконных констукций", choices=choices, )


class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        if self.fields.get('name'):
            self.fields['name'].label = u"Предмет контракта"

        if self.fields.get('summa'):
            self.fields['summa'].required = True

        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['mo'] = forms.ModelChoiceField(label=_(u'Муниципальное образование'),
                required=True, queryset=MO.objects.filter(pk=mo.pk), initial=mo.pk)
            self.fields['mo'].widget.attrs['readonly'] = 'readonly'

        auction_for_update = kwargs.get('initial').get('auction_for_update') if 'initial' in kwargs else None
        self.fields['auction_for_update'] = forms.IntegerField(initial=auction_for_update,
                                                     label=u"Контракт для обновления аукциона",
                                                     required=False, widget=forms.HiddenInput())

    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'docs')
        fields = [
           'start_year', 'finish_year', 'name', 'date', 'num', 'address',
           'flats_amount', 'area', 'developer', 'summa', 'summa_fed',
           'summa_reg', 'summ_without_mo_money', 'summ_mo_money',
           'period_of_payment', 'creation_form', 'mo', 'has_trouble_docs', 'check_result_info'
            # for remove
            # 'gas_supply', 'water_removal', 'water_settlement',
            # 'hot_water_supply', 'heating', 'electric_supply', 'public_transport',
            # 'market', 'kindergarden', 'school', 'clinic', 'is_routes', 'is_playground',
            # 'is_clother_drying', 'is_parking', 'is_dustbin_area', 'is_water_boiler',
            # 'is_heat_boiler', 'is_intercom', 'is_loggia', 'is_balcony', 'internal_doors',
            # 'entrance_door', 'window_constructions', 'floors', 'driveways',
            # 'area_cmp', 'budget',
        ]


class ResultForm(forms.ModelForm):
    recommend = forms.CharField(help_text=_(u"Рекомендации"), label=_(u'Рекомендации'), required=False,
        widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Result
        exclude = ('cmp_data', )
        fields = [
            'start_year',
            'finish_year',
            'mo',
            'mo_pers',
            'establish_pers',
            # no auction, but it present in tech doc
            'contract',
            'building',
            'readiness',
            'doc_files',
            'doc_list',
            'recommend',
            # 'room',
            # 'wc',
            # 'hallway',
            # 'kitchen',
            # 'ground',

            # for remove
            # 'check_date',
        ]

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['mo'] = forms.ModelChoiceField(label=_(u'Муниципальное образование'),
                required=True, queryset=MO.objects.filter(pk=mo.pk), initial=mo.pk)
            self.fields['mo'].widget.attrs['readonly'] = 'readonly'
            self.fields['contract'] = forms.ModelChoiceField(queryset=Contract.objects.filter(mo=mo),
                         label=_(u"Контракт"), help_text=_(u"Контракт"), required=True)
            self.fields['building'] = forms.ModelChoiceField(queryset=Building.objects.filter(mo=mo),
                         label=_(u"Объект"), help_text=_(u"Объект"), required=True)


class ContractDocumentsForm(forms.ModelForm):

    class Meta:
        model = ContractDocuments
        fields = ['mun_contracts']


class AuctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = CSIMultipleChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
                                        widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = CSIMultipleChoiceField(label=_(u"Материал входной двери"), required=False,
                                               widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = CSIMultipleChoiceField(label=_(u"Материал оконных конструкций"), required=False,
                                                  widget=CSICheckboxSelectMultiple, choices=choices)

        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['mo'] = forms.ModelChoiceField(label=_(u'Муниципальное образование'),
                required=True, queryset=MO.objects.filter(pk=mo.pk), initial=mo.pk)
            self.fields['mo'].widget.attrs['readonly'] = 'readonly'
            self.fields['contract'] = forms.ModelChoiceField(label=_(u'Данные по заключенному контракту'),
                                                             required=True, queryset=mo.contract_set.all())

    electric_supply = CSIMultipleChoiceField(label=_(u"Электроснабжение"), required=False,
                                           widget=CSICheckboxSelectMultiple, choices=ELECTRIC_SUPPLY_CHOICES)
    water_removal = CSIMultipleChoiceField(label=_(u"Водоотведение"), required=False,
                                           widget=CSICheckboxSelectMultiple, choices=WATER_REMOVAL_CHOICES)
    water_settlement = CSIMultipleChoiceField(label=_(u"Водоподведение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = CSIMultipleChoiceField(label=_(u"Горячее водоснабжение"), required=False,
                                              widget=CSICheckboxSelectMultiple, choices=HOT_WATER_SUPPLY_CHOICES)
    heating = CSIMultipleChoiceField(label=_(u"Отопление"), required=False,
                                     widget=CSICheckboxSelectMultiple, choices=HEATING_CHOICES)


    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen')

        fields = [
            'start_year', 'finish_year', 'name', 'num', 'flats_amount',
            'area_cmp', 'area', 'start_price', 'date', 'open_date',
            'proposal_count', 'mo', 'stage', 'contract', 'electric_supply',
            'water_settlement', 'water_removal', 'hot_water_supply', 'heating',
            'is_heat_boiler', 'gas_supply',
            'internal_doors', 'entrance_door', 'window_constructions',
            'is_water_boiler', 'is_loggia', 'is_balcony',
            # to remove
            # 'has_trouble_docs', 'public_transport', 'market',
            # 'kindergarden', 'school', 'clinic', 'is_routes', 'is_playground',
            # 'is_clother_drying', 'is_parking', 'is_dustbin_area', 'floors',
            # 'driveways', 'is_intercom',
        ]

    def clean(self):
        cd = super(AuctionForm, self).clean()
        mo = cd.get('mo')
        cmp_date = cd.get('public_date')
        if mo and cmp_date and mo.departamentagreement_set.filter(date__gt=cmp_date):
            msg = _(u'Дата подписания соглашения с министерством еще не наступила')
            self._errors["public_date"] = self.error_class([msg])
            del cd["public_date"]
        return cd


class PersonForm(forms.ModelForm):
    position = forms.CharField(help_text=_(u"Должность"), label=_(u'Должность'), required=False,
                               widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Person


class AuctionShowForm(forms.ModelForm):
    electric_supply = CSIMultipleChoiceField(label=_(u"Электроснабжение"), required=False,
        widget=CSICheckboxSelectMultiple, choices=ELECTRIC_SUPPLY_CHOICES)
    water_removal = CSIMultipleChoiceField(label=_(u"Водоотведение"), required=False,
        widget=CSICheckboxSelectMultiple, choices=WATER_REMOVAL_CHOICES)
    water_settlement = CSIMultipleChoiceField(label=_(u"Водоподведение"), required=False,
        widget=CSICheckboxSelectMultiple, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = CSIMultipleChoiceField(label=_(u"Горячее водоснабжение"), required=False,
        widget=CSICheckboxSelectMultiple, choices=HOT_WATER_SUPPLY_CHOICES)
    heating = CSIMultipleChoiceField(label=_(u"Отопление"), required=False,
        widget=CSICheckboxSelectMultiple, choices=HEATING_CHOICES)

    class Meta:
        model = Auction
        exclude = ('room', 'hallway', 'wc', 'kitchen',)
        fields = [
            'start_year', 'finish_year', 'name', 'num', 'flats_amount',
            'area_cmp', 'area', 'start_price', 'date', 'open_date',
            'proposal_count', 'mo', 'stage', 'contract', 'electric_supply',
            'water_settlement', 'water_removal', 'hot_water_supply', 'heating',
            'is_heat_boiler', 'gas_supply',
            'internal_doors', 'entrance_door', 'window_constructions',
            'is_water_boiler', 'is_loggia', 'is_balcony',
            # to remove
            # 'has_trouble_docs', 'public_transport', 'market',
            # 'kindergarden', 'school', 'clinic', 'is_routes', 'is_playground',
            # 'is_clother_drying', 'is_parking', 'is_dustbin_area', 'floors',
            # 'driveways', 'is_intercom',
            ]

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionShowForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = CSIMultipleChoiceField(label=_(u"Материал межкомнатных дверей"), required=False,
            widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = CSIMultipleChoiceField(label=_(u"Материал входной двери"), required=False,
            widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = CSIMultipleChoiceField(label=_(u"Материал оконных конструкций"), required=False,
            widget=CSICheckboxSelectMultiple, choices=choices)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            cmp_multi(self, cmp_initial)


class ContractShowForm(ContractForm):

    class Meta:
        model = Contract
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'auction_for_update')

        fields = [
            'start_year', 'finish_year', 'name', 'date', 'num', 'address',
            'flats_amount', 'area', 'developer', 'summa', 'summa_fed',
            'summa_reg', 'summ_without_mo_money', 'summ_mo_money',
            'period_of_payment', 'creation_form', 'mo', 'has_trouble_docs', 'check_result_info'
            # for remove
            #'has_trouble_docs', 'gas_supply', 'water_removal', 'water_settlement',
            #'hot_water_supply', 'heating', 'electric_supply', 'public_transport',
            #'market', 'kindergarden', 'school', 'clinic', 'is_routes', 'is_playground',
            #'is_clother_drying', 'is_parking', 'is_dustbin_area', 'is_water_boiler',
            #'is_heat_boiler', 'is_intercom', 'is_loggia', 'is_balcony', 'internal_doors',
            #'entrance_door', 'window_constructions', 'floors', 'driveways',
            # 'budget',
            ]

    def __init__(self, *args, **kwargs):
        self.cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(ContractShowForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

        if self.cmp_initial:
            for field in self.fields:
                if hasattr(self.instance, field) and hasattr(self.cmp_initial, field):
                    if getattr(self.instance, field) != getattr(self.cmp_initial, field):
                        self.fields[field].widget.attrs['style'] = 'background-color: red;'



class CompareDataShowForm(forms.ModelForm):
    water_settlement = forms.ChoiceField(label=_(u"Водоподведение111"), required=False,
        widget=forms.Select, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = forms.ChoiceField(label=_(u"Горячее водоснабжение"), required=False,
        widget=forms.Select, choices=HOT_WATER_SUPPLY_CHOICES)

    class Meta:
        model = CompareData
        exclude = ('room', 'hallway', 'wc', 'kitchen')

    def __init__(self, *args, **kwargs):
        super(CompareDataShowForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = forms.ChoiceField(label=u"Материал межкомнатных дверей", choices=choices,  required=False)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = forms.ChoiceField(label=u"Материал входной двери", choices=choices, required=False)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = forms.ChoiceField(label=u"Материал оконных констукций", choices=choices, required=False)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class ResultShowForm(forms.ModelForm):

    class Meta:
        model = Result
        exclude = ('cmp_data', 'room', 'wc', 'hallway', 'kitchen')

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


class FilterAuctionForm(forms.Form):
    num = forms.IntegerField(label=_(u'Номер для поиска '), required=False)

    def __init__(self, *args, **kwargs):
        super(FilterAuctionForm, self).__init__(*args, **kwargs)
        self.fields['num'].widget.attrs['class'] = "span3 search-query"
        self.fields['num'].widget.attrs['style'] = "height: 26px;"

    def clean(self):
        cd = super(FilterAuctionForm, self).clean()
        serial = cd.get('num')
        if serial and len(str(serial)) < 3:
            msg = _('Only from 3 digits search is allowed.')
            self._errors["num"] = self.error_class([msg])
            del cd["num"]
        return cd
