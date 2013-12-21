# -*- coding: utf-8 -*-
from django import template

from apps.core.forms import CSICheckboxSelectMultiple

register = template.Library()


@register.filter(name="check_divison")
def divide(value, arg):
    return str(int(value) % int(arg))


@register.filter
def get_choice_or_value(form, field_name):
    if form.initial:
        if hasattr(form.fields[field_name], "choices"):
            if form.initial.get(field_name):
                # get multichoice from form
                if isinstance(form.fields[field_name].widget, CSICheckboxSelectMultiple):
                    choices = dict(form.fields[field_name].choices)
                    val = ""
                    for v in form.initial[field_name].split(","):
                        # skip "Not set"
                        if int(v) == 0:
                            continue
                        val += " %s " % choices.get(int(v))
                    return val
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

