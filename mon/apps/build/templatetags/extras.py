from django import template

register = template.Library()

@register.filter(name="check_divison")
def divide(value, arg):
    return str(int(value) % int(arg))