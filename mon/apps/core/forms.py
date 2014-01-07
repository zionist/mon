# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.db.models import CommaSeparatedIntegerField
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from django.forms import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple

from .models import Room, WC, Hallway, Kitchen, AuctionRoom, AuctionWC, AuctionHallway, \
    AuctionKitchen, Developer, Choices
from apps.core.models import STOVE_CHOICES, SEPARATE_CHOICES


def cmp_single(obj, cmp_obj):
    for field in obj.fields:
        if hasattr(obj.instance, field) and hasattr(cmp_obj, field):
            if getattr(obj.instance, field) != getattr(cmp_obj, field):
                obj.fields[field].widget.attrs['style'] = 'background-color: red;'
        elif hasattr(obj.instance, field) and not hasattr(cmp_obj, field):
            obj.fields[field].widget.attrs['style'] = 'background-color: red;'


def cmp_multi(obj, cmp_obj):
    for field in obj.fields:
        if hasattr(obj.fields[field], 'widget') and not hasattr(obj.fields[field].widget.attrs, 'hidden'):
            if isinstance(obj.fields[field].widget, CSICheckboxSelectMultiple):
                if getattr(cmp_obj, field) and str(getattr(cmp_obj, field)) not in getattr(obj.instance, field):
                    obj.fields[field].widget.attrs['style'] = 'background-color: red;'
                    #if field == "water_settlement":
                    #    print "%s in %s" % (str(getattr(cmp_obj, field)), getattr(obj.instance, field))
                else:
                    obj.fields[field].widget.attrs['style'] = 'background-color: red;'

            elif hasattr(obj.instance, field) and hasattr(cmp_obj, field)\
                 and not isinstance(obj.fields[field].widget, CSICheckboxSelectMultiple) and not isinstance(getattr(obj.instance, field), CommaSeparatedIntegerField):
                if getattr(obj.instance, field) != getattr(cmp_obj, field):
                    obj.fields[field].widget.attrs['style'] = 'background-color: red;'


class CSICheckboxSelectMultiple(SelectMultiple):
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
        self.verbose_name = _(u"Добавление застройщика(владельца)")
        for field in self.fields:
            if hasattr(self.fields[field], 'widget') \
                and not hasattr(self.fields[field].widget.attrs, 'hidden') \
                and not isinstance(self.fields[field].widget, forms.Textarea):
                self.fields[field].widget.attrs['class'] = 'span5'
                self.fields[field].widget.attrs['style'] = 'height:26px;'


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.verbose_name = _(u"Комната")
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = forms.ChoiceField(label=u"Материал отделки пола", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = forms.ChoiceField(label=u"Материал отделки стен", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = forms.ChoiceField(label=u"Материал отделки потолка", choices=choices, )


class HallwayForm(forms.ModelForm):

    class Meta:
        model = Hallway

    def __init__(self, *args, **kwargs):
        super(HallwayForm, self).__init__(*args, **kwargs)
        self.verbose_name = _(u"Коридор")
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = forms.ChoiceField(label=u"Материал отделки пола", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = forms.ChoiceField(label=u"Материал отделки стен", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = forms.ChoiceField(label=u"Материал отделки потолка", choices=choices, )


class WCForm(forms.ModelForm):

    class Meta:
        model = WC

    def __init__(self, *args, **kwargs):
        super(WCForm, self).__init__(*args, **kwargs)
        self.verbose_name = _(u"Санузел")
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = forms.ChoiceField(label=u"Материал отделки пола", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = forms.ChoiceField(label=u"Материал отделки стен", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = forms.ChoiceField(label=u"Материал отделки потолка", choices=choices, )


class KitchenForm(forms.ModelForm):

    class Meta:
        model = Kitchen

    def __init__(self, *args, **kwargs):
        super(KitchenForm, self).__init__(*args, **kwargs)
        self.verbose_name = _(u"Кухня")
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = forms.ChoiceField(label=u"Материал отделки пола", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = forms.ChoiceField(label=u"Материал отделки стен", choices=choices, )
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = forms.ChoiceField(label=u"Материал отделки потолка", choices=choices, )


class RoomShowForm(RoomForm):

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


class HallwayShowForm(HallwayForm):

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


class WCShowForm(WCForm):

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


class KitchenShowForm(KitchenForm):

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
    def __init__(self, *args, **kwargs):
        super(BaseAuctionRoomForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = CSIMultipleChoiceField(label=_(u"Материал отделки пола"), required=False,
                                       widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = CSIMultipleChoiceField(label=_(u"Материал отделки стен"), required=False,
                                      widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = CSIMultipleChoiceField(label=_(u"Материал отделки потолка"), required=False,
                                         widget=CSICheckboxSelectMultiple, choices=choices)

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

    def __init__(self, *args, **kwargs):
        super(BaseAuctionRoomShowForm, self).__init__(*args, **kwargs)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="FLOOR_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['floor'] = CSIMultipleChoiceField(label=_(u"Материал отделки пола"), required=False,
                                                      widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="WALL_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['wall'] = CSIMultipleChoiceField(label=_(u"Материал отделки стен"), required=False,
                                                     widget=CSICheckboxSelectMultiple, choices=choices)
        choices = [(c.get("num"), c.get("value")) for c in Choices.objects.get(name="CEILING_CHOICES").choice_set.order_by("num").values('num', 'value')]
        self.fields['ceiling'] = CSIMultipleChoiceField(label=_(u"Материал отделки потолка"), required=False,
                                                        widget=CSICheckboxSelectMultiple, choices=choices)

    class Meta:
        abstract = True


class AuctionRoomShowForm(BaseAuctionRoomShowForm):

    class Meta:
        model = AuctionRoom

    def __init__(self, *args, **kwargs):

        cmp_initial = kwargs.pop('cmp_initial') if kwargs.get('cmp_initial') else None
        super(AuctionRoomShowForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if hasattr(self.fields[field], 'widget') and not hasattr(self.fields[field].widget.attrs, 'hidden'):
                self.fields[field].widget.attrs['disabled'] = 'disabled'
        if cmp_initial:
            cmp_single(self, cmp_initial)


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
            cmp_single(self, cmp_initial)


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
            cmp_multi(self, cmp_initial)


class ChoicesForm(forms.ModelForm):

    class Meta:
        model = Choices
        exclude = ['name']