# -*- coding: utf-8 -*-
from django import template

from django.forms import SelectMultiple
from apps.core.forms import CSICheckboxSelectMultiple
from django.forms import DateInput

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
                elif isinstance(form.fields[field_name].widget, SelectMultiple):
                    print('SelectMultiple', dict(form.fields[field_name].choices))
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
    return field


@register.filter
def get_field_for_cmp(form, field_name):
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
        return form.initial.get(field_name)

@register.filter
def get_element_by_index(l, index):
    return l[int(index)]
