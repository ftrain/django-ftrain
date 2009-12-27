from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def tabularize(value, cols):
    """modifies a list to become a list of lists
    eg [1,2,3,4] becomes [[1,2], [3,4]] with an argument of 2"""
    try:
        cols = int(cols)
    except ValueError:
        return [value]
    return map(*([None] + [value[i::cols] for i in range(0,cols)])) 

@register.filter
@stringfilter
def smartypants(value):
    try:
        import smartypants
        return smartypants.smartyPants(value, 'qd')
    except ImportError:
        return value
