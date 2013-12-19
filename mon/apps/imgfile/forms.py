# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from apps.cmp.models import MO
from apps.cmp.models import Person
from apps.cmp.models import Auction, Contract
from apps.core.models import YES_NO_CHOICES

from .models import Image, File


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image


class FileForm(forms.ModelForm):
    class Meta:
        model = File


class SelectMoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectMoForm, self).__init__(*args, **kwargs)
        choices = [(mo.id, mo.name) for mo in MO.objects.all()]
        self.fields['mo'] = forms.ChoiceField(label=u"Муниципальное образование",
                               choices=choices)


class QuestionsListForm(forms.Form):

    def __init__(self, mo, *args, **kwargs):
        super(QuestionsListForm, self).__init__(*args, **kwargs)
        self.fields['mo'] = forms.CharField(initial=mo.name,
            label=u"Муниципальное образование",
            widget=forms.TextInput(attrs={'readonly': True}))
        choices = [(a.get('id'), a.get('num'))
                   for a in Auction.objects.filter(mo=mo.pk).values('id', 'num')]
        choices.insert(0, ("", u"----"))
        self.fields['auction'] = forms.ChoiceField(label=u"Аукцион", required=True,
                                                   choices=choices)
        self.fields['responsible_person'] = forms.CharField(
            label=u"Исполнитель работ от муниципального образования")
        choices = [(p.id, p.name) for p in Person.objects.all()]
        self.fields['persons_list'] = forms.MultipleChoiceField(
            label=u"Список участников осмотра",
            choices=choices)
        choices = []
        self.fields['objects_equal'] = forms.ChoiceField(choices=YES_NO_CHOICES,
                                                    label=u"Все объекты типовые")
        self.fields['list_sent_to_mo'] = forms.ChoiceField(choices=YES_NO_CHOICES,
            label=u"Направлен ли список граждан, подлежащих обеспечению жилыми помещениями в муниципальное образование (информация уточняется предварительно в отделе управления государственной информационной системой)")
