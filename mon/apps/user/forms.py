# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, modelform_factory, BaseModelFormSet
from apps.user.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'mo']
    is_staff = forms.NullBooleanField(required=False, label=_(u'Назначить права админа'))


class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        exclude = ('user_permissions', 'is_superuser')
