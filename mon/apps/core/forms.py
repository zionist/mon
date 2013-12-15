# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from django.forms import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from .models import Room, WC, Hallway, Kitchen, AuctionRoom, AuctionWC, AuctionHallway, AuctionKitchen, Developer
from apps.core.models import FLOOR_CHOICES, WALL_CHOICES, CEILING_CHOICES, STOVE_CHOICES, SEPARATE_CHOICES


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


class DeveloperForm(forms.ModelForm):
    boss_position = forms.CharField(help_text=_(u"Ф.И.О. и должность руководителя"), required=False,
                                    label=_(u'Ф.И.О. и должность руководителя'), widget=forms.Textarea(attrs={'rows': 4}))
    address = forms.CharField(help_text=_(u"Фактический адрес"), label=_(u'Фактический адрес'), required=False,
                              widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Developer
        exclude = ('doc', 'image')

    def __init__(self, *args, **kwargs):
        super(DeveloperForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') \
                and not hasattr(self.fields[field].widget.attrs, 'hidden') \
                and not isinstance(self.fields[field].widget, forms.Textarea):
                self.fields[field].widget.attrs['class'] = 'span5'
                self.fields[field].widget.attrs['style'] = 'height:26px;'


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room


class HallwayForm(forms.ModelForm):

    class Meta:
        model = Hallway


class WCForm(forms.ModelForm):

    class Meta:
        model = WC


class KitchenForm(forms.ModelForm):

    class Meta:
        model = Kitchen


class RoomShowForm(forms.ModelForm):

    class Meta:
        model = Room

    def __init__(self, *args, **kwargs):

        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(RoomShowForm, self).__init__(*args, **kwargs)

        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class HallwayShowForm(forms.ModelForm):

    class Meta:
        model = Hallway

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(HallwayShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class WCShowForm(forms.ModelForm):

    class Meta:
        model = WC

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(WCShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class KitchenShowForm(forms.ModelForm):

    class Meta:
        model = Kitchen

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(KitchenShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class BaseAuctionRoomForm(forms.ModelForm):
    floor = CSIMultipleChoiceField(label=_(u"Материал отделки пола"), required=False,
                                   widget=CSICheckboxSelectMultiple, choices=FLOOR_CHOICES)
    wall = CSIMultipleChoiceField(label=_(u"Материал отделки стен"), required=False,
                                  widget=CSICheckboxSelectMultiple, choices=WALL_CHOICES)
    ceiling = CSIMultipleChoiceField(label=_(u"Материал отделки потолка"), required=False,
                                     widget=CSICheckboxSelectMultiple, choices=CEILING_CHOICES)

    class Meta:
        abstract = True


class AuctionRoomForm(BaseAuctionRoomForm):

    class Meta:
        model = AuctionRoom


class AuctionHallwayForm(BaseAuctionRoomForm):

    class Meta:
        model = AuctionHallway


class AuctionWCForm(BaseAuctionRoomForm):
    separate = CSIMultipleChoiceField(label=_(u"Санузел"), required=False,
                                      widget=CSICheckboxSelectMultiple, choices=SEPARATE_CHOICES)

    class Meta:
        model = AuctionWC


class AuctionKitchenForm(BaseAuctionRoomForm):
    stove = CSIMultipleChoiceField(label=_(u"Кухонная плита"), required=False,
                                   widget=CSICheckboxSelectMultiple, choices=STOVE_CHOICES)

    class Meta:
        model = AuctionKitchen


class BaseAuctionRoomShowForm(forms.ModelForm):
    floor = CSIMultipleChoiceField(label=_(u"Материал отделки пола"), required=False,
                                   widget=CSICheckboxSelectMultiple, choices=FLOOR_CHOICES)
    wall = CSIMultipleChoiceField(label=_(u"Материал отделки стен"), required=False,
                                  widget=CSICheckboxSelectMultiple, choices=WALL_CHOICES)
    ceiling = CSIMultipleChoiceField(label=_(u"Материал отделки потолка"), required=False,
                                     widget=CSICheckboxSelectMultiple, choices=CEILING_CHOICES)

    class Meta:
        abstract = True


def cmp_single(obj, cmp_obj):
    for field in obj.fields:
        if getattr(obj.instance, field) != getattr(cmp_obj, field):
            obj.fields[field].widget.attrs['style'] = 'background-color: red;'


def cmp_multi(obj, cmp_obj):
    for field in obj.fields:
        if hasattr(obj.fields[field], 'widget') and not hasattr(obj.fields[field].widget.attrs, 'hidden') \
            and isinstance(obj.fields[field].widget, 'CSICheckboxSelectMultiple'):
            if getattr(obj.instance, field) not in getattr(cmp_obj, field):
                obj.fields[field].widget.attrs['style'] = 'background-color: red;'
        else:
            if getattr(obj.instance, field) != getattr(cmp_obj, field):
                obj.fields[field].widget.attrs['style'] = 'background-color: red;'


class AuctionRoomShowForm(BaseAuctionRoomShowForm):

    class Meta:
        model = AuctionRoom

    def __init__(self, *args, **kwargs):

        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionRoomShowForm, self).__init__(*args, **kwargs)

        if cmp_initial:
            cmp_single(self, cmp_initial)
            #for field in self.fields:
            #    if getattr(self.instance, field) != getattr(cmp_initial, field):
            #        self.fields[field].widget.attrs['style'] = 'background-color: red;'

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class AuctionHallwayShowForm(BaseAuctionRoomShowForm):

    class Meta:
        model = AuctionHallway

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionHallwayShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'


class AuctionWCShowForm(BaseAuctionRoomShowForm):
    separate = CSIMultipleChoiceField(label=_(u"Санузел"), required=False,
                                      widget=CSICheckboxSelectMultiple, choices=SEPARATE_CHOICES)

    class Meta:
        model = AuctionWC

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionWCShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            cmp_multi(self, cmp_initial)
            #for field in self.fields:
            #    if getattr(self.instance, field) != getattr(cmp_initial, field):
            #        self.fields[field].widget.attrs['style'] = 'background-color: red;'


class AuctionKitchenShowForm(BaseAuctionRoomShowForm):
    stove = CSIMultipleChoiceField(label=_(u"Кухонная плита"), required=False,
                                   widget=CSICheckboxSelectMultiple, choices=STOVE_CHOICES)

    class Meta:
        model = Kitchen

    def __init__(self, *args, **kwargs):
        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionKitchenShowForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            for field in self.fields:
                if getattr(self.instance, field) != getattr(cmp_initial, field):
                    self.fields[field].widget.attrs['style'] = 'background-color: red;'
