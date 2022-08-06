from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    return str(text).startswith(starts)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
