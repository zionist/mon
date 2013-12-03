from django import template

register = template.Library()


@register.filter(name="check_divison")
def divide(value, arg):
    return str(int(value) % int(arg))


@register.filter
def get_choice_or_value(form, field_name):
    if hasattr(form.fields[field_name], "choices"):
        # print form.fields[field_name].__dict__
        if form.initial[field_name] is not None:
            choices = dict(form.fields[field_name].choices)
            return choices.get(form.initial[field_name])
    else:
        return form.initial[field_name]
