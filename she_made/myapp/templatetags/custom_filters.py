from django import template

register = template.Library()

@register.filter(name='split_at_colon')
def split_at_colon(value):
    parts = value.split(':', 1)
    return parts[0], parts[1] if len(parts) > 1 else None

@register.filter(name='split_at_question_mark')
def split_at_question_mark(value):
    parts = value.split('?', 1)
    question = parts[0].strip() + '?' if len(parts) > 1 else value.strip()
    answer = parts[1].strip() if len(parts) > 1 else None
    return question, answer

@register.filter(name='in_list')
def in_list(value, arg):
    return value in arg

@register.filter(name='replace_spaces_with_plus') 
def replace_spaces_with_plus(value):
    return value.replace(' ', '+')  