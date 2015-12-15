from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def formfield(value, arg):
    if ',' in arg:
        size, units = arg.split(',')
    else:
        size = arg
        units = None
    return render_to_string('lifting/_form-group.html',
                            {'field': value, 'size': size, 'units': units})
