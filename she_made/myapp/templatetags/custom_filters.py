from django import template

register = template.Library()

@register.filter(name='split_at_colon')
def split_at_colon(value):
    parts = value.split(':', 1)
    return parts[0], parts[1] if len(parts) > 1 else None