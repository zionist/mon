# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.translation import ugettext_lazy as _

from django.forms import SelectMultiple
from django.forms import DateInput, DateTimeInput
from django.utils.safestring import SafeText

from apps.core.forms import CSICheckboxSelectMultiple

register = template.Library()


@register.filter(name="check_divison")
def divide(value, arg):
    return str(int(value) % int(arg))


@register.filter
def get_choice_or_value(form, field_name):
    if form.initial:
        if hasattr(form.fields[field_name], "choices"):
            if form.initial.get(field_name) is not None:
                # get multichoice from form
                if isinstance(form.fields[field_name].widget, CSICheckboxSelectMultiple):
                    choices = dict(form.fields[field_name].choices)
                    print('    choices', choices, form.initial[field_name].split(","))
                    val = ""
                    for v in form.initial[field_name].split(","):
                        # skip "Not set"
                        try:
                            choice = choices.get(int(v))
                        except ValueError:
                            return None
                        val += " %s " % choice
                    return val
                elif isinstance(form.fields[field_name].widget, SelectMultiple):
                    choices = list(form.fields[field_name].choices)
                    return '; '.join([x[1] for x in choices])
                else:
                    choices = dict(form.fields[field_name].choices)
                    return choices.get(form.initial[field_name])
        else:
            return form.initial.get(field_name)
    elif form.data:
        if hasattr(form.fields[field_name], "choices"):
            if form.data.get(field_name) is not None:
                choices = dict(form.fields[field_name].choices)
                return choices.get(form.data[field_name])
        else:
            return form.data.get(field_name)


@register.filter
def yes_no_rus(value):
    if isinstance(value, SafeText) or isinstance(value, str):
        m = re.search('<span\s*class="text-error">(.*?)</span>', value)
        if m:
            if "True" in m.group(1):
                return re.sub("True", u"Да", value)
            if "False" in m.group(1):
                return re.sub("False", u"Нет", value)
    if value == True:
        return u"Да"
    elif value == False:
        return u"Нет"
    else:
        return value

@register.filter
def dict_val(d, key):
    try:
        d[key]
    except KeyError:
        return ''
    return d[key]

@register.filter
def add_date_mask_class(field):
    if isinstance(field.field.widget, DateInput):
        field.field.widget.attrs.update({'class': 'date_mask',
                                         'placeholder': 'день.месяц.год'})
    if isinstance(field.field.widget, DateTimeInput):
        field.field.widget.attrs.update({'class': 'date_time_mask',
                                         'placeholder': 'день.месяц.год час:минута'})
    return field


@register.filter
def get_field_for_cmp(form, field_name):
    if hasattr(form.fields[field_name], "choices"):
        if form.initial.get(field_name) is not None:
            # get multichoice from form
            if isinstance(form.fields[field_name].widget, CSICheckboxSelectMultiple):
                choices = dict(form.fields[field_name].choices)
                val = ""
                for v in form.initial[field_name].split(","):
                    # skip "Not set"
                    try:
                        if int(v) == 0:
                            continue
                    except ValueError:
                        return None
                    val += " %s " % choices.get(int(v))
                # set error style for text
                field = form.fields[field_name]
                if field.widget.attrs.get("style"):
                    if "background-color: red;" in field.widget.attrs.get("style"):
                        return '<span class="text-error"> %s </span>' % val
                return val
            elif isinstance(form.fields[field_name].widget, SelectMultiple):
                choices = list(form.fields[field_name].choices)
                val = '; '.join([x[1] for x in choices])
                # set error style for text
                field = form.fields[field_name]
                if field.widget.attrs.get("style"):
                    if "background-color: red;" in field.widget.attrs.get("style"):
                        return '<span class="text-error"> %s </span>' % val
                return val
            else:
                choices = dict(form.fields[field_name].choices)
                field = form.fields[field_name]
                val = choices.get(form.initial[field_name])
                if field.widget.attrs.get("style"):
                    if "background-color: red;" in field.widget.attrs.get("style"):
                        return '<span class="text-error"> %s </span>' % val
                return val
    else:
        val = form.initial.get(field_name)
        field = form.fields[field_name]
        if field.widget.attrs.get("style"):
            if "background-color: red;" in field.widget.attrs.get("style"):
                if val is not None:
                    return '<span class="text-error"> %s </span>' % val
                else:
                    return '<span class="text-error"> %s </span>' % u"Не указано"
        return val

@register.filter
def get_element_by_index(l, index):
    return l[int(index)]
