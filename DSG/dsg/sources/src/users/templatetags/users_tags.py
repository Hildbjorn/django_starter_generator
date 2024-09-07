import json
from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe
from typus import ru_typus

register = template.Library()


@register.simple_tag
def verbose_name(instance, field_name):
    """ Returns verbose_name for a field. """
    return str(ru_typus(instance._meta.get_field(field_name).verbose_name))


@register.filter(is_safe=True)
def replace_n(value):
    if value is not None and isinstance(value, str):
        return value.replace('\n', '<br />')
    else:
        return value


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(is_safe=True)
def replace_comma(value):
    if value is not None:
        return value.replace(',', '.')
    else:
        pass


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter(name="typus", is_safe=True)
def typus(value):
    return ru_typus(value)


@register.simple_tag()
def my_set(value):
    return value


@register.filter(name="without_quotes", is_safe=True)
def without_quotes(value):
    if value.startswith('"'):
        value = value[:1]
    else:
        value = value
    if value.endswith('"'):
        value = value[:-1]
    else:
        value = value
    return ru_typus(value)
