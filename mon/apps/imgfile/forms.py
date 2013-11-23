# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet

from .models import Image, File


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image


class FileForm(forms.ModelForm):
    class Meta:
        model = File
