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

from .models import Image, File


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image


class FileForm(forms.ModelForm):
    class Meta:
        model = File


class SelectMoForm(forms.Form):
    choices = [(mo.id, mo.name) for mo in MO.objects.all()]
    mo = forms.ChoiceField(label=u"Муниципальное образование",
                           choices=choices)


class QuestionsListForm(forms.Form):

    def __init__(self, mo, *args, **kwargs):
        super(QuestionsListForm, self).__init__(*args, **kwargs)
        self.fields['mo'] = forms.CharField(initial=mo.name,
            label=u"Муниципальное образование",
            widget=forms.TextInput(attrs={'readonly': True}))
        choices = [(a.id, a.num) for a in Auction.objects.filter(mo=mo.pk)]
        choices.insert(0, (0, u"----"))
        self.fields['auction'] = forms.ChoiceField(label=u"Аукцион",
                                                   choices=choices)
        choices = [(c.id, c.num) for c in Contract.objects.filter(mo=mo.pk)]
        choices.insert(0, (0, u"----"))
        self.fields['contract'] = forms.ChoiceField(label=u"Контракт",
                                                 choices=choices)

    responsible_person = forms.CharField(
        label=u"Исполнитель работ от муниципального образования")
    choices = [(p.id, p.name) for p in Person.objects.all()]
    persons_list = forms.MultipleChoiceField(
        label=u"Список участников осмотра",
        choices=choices)
