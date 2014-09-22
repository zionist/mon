# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
import autocomplete_light

from .models import Building, Ground
from apps.core.models import STATE_CHOICES, BUILD_STATE_CHOICES, \
    WATER_SETTLEMENT_CHOICES, HOT_WATER_SUPPLY_CHOICES, Developer, READINESS_CHOICES
from apps.core.forms import cmp_single
from apps.build.models import Contract
from apps.core.models import Choices
from apps.mo.models import MO


class GroundForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroundForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = forms.ChoiceField(label=u"Материал межкомнатных дверей", choices=choices, required=False)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = forms.ChoiceField(label=u"Материал входной двери", choices=choices, required=False)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = forms.ChoiceField(label=u"Материал оконных констукций", choices=choices, required=False)
        self.fields['contract'] = forms.ModelChoiceField(queryset=Contract.objects.all(),
           label=_(u"Контракт"), help_text=_(u"Контракт"), required=True)

        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['contract'] = forms.ModelChoiceField(queryset=Contract.objects.filter(mo=mo),
                                                             label=_(u"Контракт"), help_text=_(u"Контракт"), required=True)
            self.fields['mo'] = forms.ModelChoiceField(label=_(u'Муниципальное образование'), required=True,
                                                       queryset=MO.objects.filter(pk=mo.pk), initial=mo.pk)
            self.fields['mo'].widget.attrs['readonly'] = 'readonly'
            self.fields['contract'] = forms.ModelChoiceField(label=_(u'Контракт'), required=True,
                                                             queryset=mo.contract_set.all())

    water_settlement = forms.ChoiceField(label=_(u"Водоподведение"), required=False,
        widget=forms.Select, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = forms.ChoiceField(label=_(u"Горячее водоснабжение"), required=False,
        widget=forms.Select, choices=HOT_WATER_SUPPLY_CHOICES)

    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4 }))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), required=False, widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'developer',
                   'state', 'approve_status')


class GroundUpdateForm(GroundForm):

    def __init__(self, *args, **kwargs):
        super(GroundUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'state',
                   'approve_status', 'flats_amount')


class BuildingForm(GroundForm):

    def __init__(self, *args, **kwargs):


        build_state = kwargs.get('initial').get('build_state') if 'initial' in kwargs else None

        def _validate_readiness(value):
            if not build_state:
                raise ValidationError(u'Степень готовности должа быть "Сдан в эксплуатацию"')
            else:
                if int(value) != 5 and int(build_state) == 2:
                    raise ValidationError(u'Степень готовности должна быть "Сдан в эксплуатацию"')

        super(BuildingForm, self).__init__(*args, **kwargs)

        self.fields['readiness'] = forms.ChoiceField(choices=READINESS_CHOICES,
                                                     validators=[_validate_readiness, ],
                                                     label=u'Степень готовности')
        self.fields['contract'].required = True
        self.ownership = None
        if build_state and int(build_state) == 2:
            self.ownership = True
            for name in ['ownership_year', 'ownership_num', 'cad_num', 'cad_sum',  'floor',
                         'mo_fond_doc_date',  'mo_fond_doc_num', ]:
                self.fields[name].required = True
        if not self.ownership:
            for name in ['ownership_year', 'ownership_num', 'build_year', 'cad_num', 'cad_sum',  'floor',
                'mo_fond_doc_date',  'mo_fond_doc_num', ]:
                self.fields.pop(name)
        self.fields['build_state'].widget = forms.HiddenInput()

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'state', 'approve_status', 'flats_amount', )
        fields = [
            'start_year', # Срок начала учета в системе
            'finish_year', # Срок окончания учета в системе
            'readiness', # Степень готовности
            'payment_perspective', # Перспектива освоения
            'mo', # Муниципальное образование
            'address', # Адрес
            'developer', # Застройщик (владелец) объекта
            'contract', # Контракт
            'planing_floor', # Этаж (планируемый)
            'driveway_num', # Подъезд
            'area', # Общая площадь (кв. м)
            # 'area_cmp', # Общая площадь не менее/равна
            'electric_supply', # Электроснабжение
            'water_settlement', # Водоподведение
            'water_removal', # Водоотведение
            'hot_water_supply', # Горячее водоснабжение
            'heating', # Отопление
            'is_heat_boiler', # Отопительный котел
            'gas_supply', # Газоснабжение
            'internal_doors', # Материал межкомнатных дверей
            'entrance_door', # Материал входной двери
            'window_constructions', # Материал оконных констукций
            'is_water_boiler', # Водонагревательный прибор (бойлер)
            'is_loggia', # Наличие лоджии
            'is_balcony', # Наличие балкона
            'comment', # Комментарий

            'build_state', # Статус объекта
            'ownership_year', # Дата перехода права собственности
            'ownership_num', # Номер документа перехода права собственности
            'build_year', # Год постройки
            'cad_num', # Кадастровый номер
            'cad_sum', # Кадастровая стоимость, руб.
            'floor', # Этаж сданного в эксплуатацию объекта
            'mo_fond_doc_date', # Дата документа МО о передаче жилого помещения в спец. фонд
            'mo_fond_doc_num', # Номер документа МО о передаче жилого помещения в спец. фонд

            # for remove
            # 'mo_fond_doc_date', # Дата документа МО о передаче жилого помещения в спец. фонд
            # 'mo_fond_doc_num', # Номер документа МО о передаче жилого помещения в спец. фонд
            # 'public_transport', # Ближайшая остановка общественного транспорта отдаленность, м
            # 'market', # Магазин отдаленность, м
            # 'kindergarden', # Детский сад отдаленность, м
            # 'school', # Школа отдаленность, м
            # 'clinic', # Поликлиника отдаленность, м
            # 'is_routes', # Подъездные пути
            # 'is_playground', # Детская площадка
            # 'is_clother_drying', # Площадка для сушки белья
            # 'is_parking', # Парковка
            # 'is_dustbin_area', # Площадка для мусорных контейнеров
            # 'is_intercom', # Домофон
            # 'complete_date', # Срок сдачи в эксплуатацию
            # 'ownership_doc_num', # Номер документа перехода права собственности
            # 'cad_passport', # Выписка из кадастрового паспорта
            # 'floors', # Этажность
            # 'driveways', # Подъездность
            # 'flats_amount', # Количество жилых помещений
            # 'flat_num', # Номер жилого помещения
        ]


class BuildingUpdateForm(GroundForm):

    def __init__(self, *args, **kwargs):
        super(BuildingUpdateForm, self).__init__(*args, **kwargs)
        self.fields['contract'].required = True
        self.ownership = None
        if self.instance:
            if self.instance.build_state and int(self.instance.build_state) == 2:
                for name in ['ownership_year', 'ownership_num', 'cad_num', 'cad_sum',  'floor',
                             'mo_fond_doc_date',  'mo_fond_doc_num', ]:
                    self.fields[name].required = True
            else:
                for name in ['ownership_year', 'ownership_num', 'build_year', 'cad_num', 'cad_sum',  'floor',
                             'mo_fond_doc_date',  'mo_fond_doc_num', ]:
                    self.fields.pop(name)


    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'state',
        'approve_status', 'build_state')
        fields = [
            'start_year', # Срок начала учета в системе
            'finish_year', # Срок окончания учета в системе
            'readiness', # Степень готовности
            'payment_perspective', # Перспектива освоения
            'mo', # Муниципальное образование
            'address', # Адрес
            'developer', # Застройщик (владелец) объекта
            'contract', # Контракт
            'planing_floor', # Этаж (планируемый)
            'driveway_num', # Подъезд
            'area', # Общая площадь (кв. м)
             # 'area_cmp', # Общая площадь не менее/равна
            'electric_supply', # Электроснабжение
            'water_settlement', # Водоподведение
            'water_removal', # Водоотведение
            'hot_water_supply', # Горячее водоснабжение
            'heating', # Отопление
            'is_heat_boiler', # Отопительный котел
            'gas_supply', # Газоснабжение
            'internal_doors', # Материал межкомнатных дверей
            'entrance_door', # Материал входной двери
            'window_constructions', # Материал оконных констукций
            'is_water_boiler', # Водонагревательный прибор (бойлер)
            'is_loggia', # Наличие лоджии
            'is_balcony', # Наличие балкона
            'comment', # Комментарий

            'build_state', # Статус объекта
            'ownership_year', # Дата перехода права собственности
            'ownership_num', # Номер документа перехода права собственности
            'build_year', # Год постройки
            'cad_num', # Кадастровый номер
            'cad_sum', # Кадастровая стоимость, руб.
            'floor', # Этаж сданного в эксплуатацию объекта
            'mo_fond_doc_date', # Дата документа МО о передаче жилого помещения в спец. фонд
            'mo_fond_doc_num', # Номер документа МО о передаче жилого помещения в спец. фонд

            # for remove
            # 'mo_fond_doc_date', # Дата документа МО о передаче жилого помещения в спец. фонд
            # 'mo_fond_doc_num', # Номер документа МО о передаче жилого помещения в спец. фонд
            # 'public_transport', # Ближайшая остановка общественного транспорта отдаленность, м
            # 'market', # Магазин отдаленность, м
            # 'kindergarden', # Детский сад отдаленность, м
            # 'school', # Школа отдаленность, м
            # 'clinic', # Поликлиника отдаленность, м
            # 'is_routes', # Подъездные пути
            # 'is_playground', # Детская площадка
            # 'is_clother_drying', # Площадка для сушки белья
            # 'is_parking', # Парковка
            # 'is_dustbin_area', # Площадка для мусорных контейнеров
            # 'is_intercom', # Домофон
            # 'complete_date', # Срок сдачи в эксплуатацию
            # 'ownership_doc_num', # Номер документа перехода права собственности
            # 'cad_passport', # Выписка из кадастрового паспорта
            # 'floors', # Этажность
            # 'driveways', # Подъездность
            # 'flats_amount', # Количество жилых помещений
            # 'flat_num', # Номер жилого помещения
        ]


class BuildingUpdateStateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        def _validate_status(value):
            if self.instance.readiness is None:
                raise ValidationError(u'Степень готовности должна быть "Сдан в эксплуатацию"')
            else:
                print int(self.instance.readiness) != 5
                if int(self.instance.readiness) != 5 and int(value) == 2:
                    raise ValidationError(u'Степень готовности должна быть "Сдан в эксплуатацию"')
        super(BuildingUpdateStateForm, self).__init__(*args, **kwargs)
        self.fields['build_state'] = forms.ChoiceField(choices=BUILD_STATE_CHOICES, validators=[_validate_status, ],
                                                       label=u'Статус объекта')
        self.fields['build_state'].choices = BUILD_STATE_CHOICES

    class Meta:
        model = Building
        fields = ['build_state', ]


class CopyBuildingForm(BuildingForm):

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)


class CopyForm(forms.Form):
    amount = forms.IntegerField(required=True, max_value=50, min_value=1,
                                initial=1, help_text=_(u"Количество копий"),
                                label=_(u"Количество копий"))


class BuildingMonitoringForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BuildingMonitoringForm, self).__init__(*args, **kwargs)
        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['mo'].widget.attrs['readonly'] = True
            self.fields['mo'] = forms.ModelChoiceField(required=True,
               queryset=MO.objects.filter(pk=mo.pk),
               initial=mo.pk)

    class Meta:
        model = Building
        fields = ('start_year', 'finish_year', 'address', 'flats_amount', 'area', 'comment',
                  'approve_status', 'mo', 'cad_num', 'contract')


class GroundMonitoringForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroundMonitoringForm, self).__init__(*args, **kwargs)
        mo = kwargs.get('initial').get('mo') if 'initial' in kwargs else None
        if mo:
            self.fields['mo'].widget.attrs['readonly'] = True
            self.fields['mo'] = forms.ModelChoiceField(required=True,
                                                       queryset=MO.objects.filter(pk=mo.pk),
                                                       initial=mo.pk)

    class Meta:
        model = Ground
        fields = ('start_year', 'finish_year', 'address', 'area', 'cad_passport', 'comment',
                  'approve_status', 'mo', 'cad_num', 'contract')


class BuildingSelectForm(forms.Form):
    state = forms.ChoiceField(label=_(u'Тип объекта'), required=True, choices=STATE_CHOICES, help_text=_(u"Тип объекта"), )
    build_state = forms.ChoiceField(label=_(u'Статус объекта'), required=True, choices=BUILD_STATE_CHOICES, help_text=_(u"Статус объекта"), )
    developer = forms.ModelChoiceField(label=_(u'Выберите застройщика'),
        required=False, queryset=Developer.objects.all(),
        help_text=_(u"Выберите застройщика (будет предложено добавить нового при пустом значении)"), )

    def __init__(self, *args, **kwargs):
        super(BuildingSelectForm, self).__init__(*args, **kwargs)
        contract = kwargs.get('initial').get('contract') if 'initial' in kwargs else None
        self.fields['contract'] = forms.IntegerField(initial=contract,
                                                     label=u"Презаполненый контракт",
                                                     required=False, widget=forms.HiddenInput())
        self.verbose_name = _(u"Выбор типа объекта рынка жилья и застройщика(владельца)")


class BuildingSelectMonitoringForm(BuildingSelectForm):
    pass


class BuildingShowForm(BuildingForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract', 'developer', 'approve_status', 'cad_passport',
                   'area', 'address', 'comment', 'complete_date', 'payment_perspective', 'flats_amount')

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(BuildingShowForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['hidden'] = 'hidden'
        self.fields['comment'].widget.attrs['hidden'] = 'hidden'

        for field in self.fields:
            if hasattr(self.fields[field], 'widget')and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'

        if cmp_initial:
            cmp_single(self, cmp_initial)


class GroundShowForm(BuildingShowForm):

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract',
                   'address', 'comment', 'complete_date', 'readiness', 'payment_perspective')
