# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Building, Ground
from apps.core.models import STATE_CHOICES, \
    WATER_SETTLEMENT_CHOICES, HOT_WATER_SUPPLY_CHOICES, Developer
from apps.core.forms import cmp_single
from apps.core.models import Choices


class GroundForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroundForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="INTERNAL_DOORS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['internal_doors'] = forms.ChoiceField(label=u"Материал межкомнатных дверей", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="ENTRANCE_DOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['entrance_door'] = forms.ChoiceField(label=u"Материал входной двери", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WINDOW_CONSTRUCTIONS_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['window_constructions'] = forms.ChoiceField(label=u"Материал оконных констукций", choices=choices, )

    water_settlement = forms.ChoiceField(label=_(u"Водоподведение"), required=False,
        widget=forms.Select, choices=WATER_SETTLEMENT_CHOICES)
    hot_water_supply = forms.ChoiceField(label=_(u"Горячее водоснабжение"), required=False,
        widget=forms.Select, choices=HOT_WATER_SUPPLY_CHOICES)

    address = forms.CharField(help_text=_(u"Адрес"), label=_(u'Адрес'), widget=forms.Textarea(attrs={'rows': 4 }))
    comment = forms.CharField(help_text=_(u"Комментарий"), label=_(u'Комментарий'), required=False, widget=forms.Textarea(attrs={'rows': 4 }))

    class Meta:
        model = Ground
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'developer', 'state')


class BuildingForm(GroundForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'developer', 'state')


class BuildingSelectForm(forms.Form):
    state = forms.ChoiceField(label=_(u'Тип объекта'), required=True, choices=STATE_CHOICES, help_text=_(u"Тип объекта"), )
    developer = forms.ModelChoiceField(label=_(u'Выберите застройщика'),
        required=False, queryset=Developer.objects.all(),
        help_text=_(u"Выберите застройщика (будет предложено добавить нового при пустом значении)"), )


class BuildingShowForm(BuildingForm):

    class Meta:
        model = Building
        exclude = ('room', 'hallway', 'wc', 'kitchen', 'contract', 'developer', 'offer', 'permission', 'approve_status',
                   'area', 'address', 'comment', 'complete_date', 'readiness', 'payment_perspective', 'flats_amount')

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
