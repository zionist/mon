# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name="check_divison")
def divide(value, arg):
    return str(int(value) % int(arg))


@register.filter
def get_choice_or_value(form, field_name):
    if field_name == 'recommend':
        print '!!!!'
        print form.initial
        print '!!!!'
    if form.initial:
        if hasattr(form.fields[field_name], "choices"):
            if form.initial.get(field_name) is not None:
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

