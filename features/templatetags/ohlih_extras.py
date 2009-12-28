from django import template
from fractions import Fraction
from hyphen import hyphenator, dictools, config
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.conf import settings
from kcal.models import Event

import re
import os

register = template.Library()
@register.filter
def sum_calories(set_of_foods):
    "Sums calories of a given meal"
    sum = 0
    for food in set_of_foods:
        sum = sum + int(float(food.kcal) * float(Fraction(food.quantity)))
    return sum

@register.filter
def sum_daily_calories(day_list):
    "Sums calories of a given day"
    sum = 0
    for event in day_list:
        for food in event.food_set.all():
            sum = sum + int(float(food.kcal) * float(Fraction(food.quantity)))            
    return sum

@register.filter
def commas(value,arg):
    import re
    __test__ = {}
    re_digits_nondigits = re.compile(r'\d+|\D+')
        
    parts = re_digits_nondigits.findall(arg % (value,))
    for i in xrange(len(parts)):
        s = parts[i]
        if s.isdigit():
            r = []
            for j, c in enumerate(reversed(s)):
                if j and (not (j % 3)):
                    r.insert(0, ',')
                r.insert(0, c)
            parts[i] = ''.join(r)
            break
    return ''.join(parts)

@register.filter
def smartypants(value):
    try:
        import smartypants
        return smartypants.smartyPants(value)
    except:
        return value    

@register.filter
def strip_paras(value):
    return re.sub(r'<p>(.*)</p>',r'\1',value)

@register.filter
def fix_type_pre(value):
    new_value = value
    new_value = re.sub(r'---+',r'<nobr>&mdash;&mdash;</nobr>', new_value)
    new_value = re.sub(r'\.{3}[^\.]',r' <nobr> . . . </nobr> ', new_value)
    new_value = re.sub(r'\.{4}',r' <nobr> . . . . </nobr> ', new_value)
    return new_value

@register.filter
def fix_type_post(value):
    new_value = value
    new_value = re.sub(r'\&amp;',r'<i>&amp;</i>', new_value)
    new_value = re.sub(r'\Wand\W',r' <i>&amp;</i> ', new_value)
    new_value = re.sub(r'\Wetc\.',r' <i>&amp;</i>c. ', new_value)
    return new_value

# uni_fractions = {'1/2':'189',
#                  '1/3':'8531',
#                  '2/3':'8532', 
#                  '1/4':'188',
#                  '3/4':'190',
#                  '1/5':'8533',
#                  '2/5':'8534',
#                  '3/5':'8535',
#                  '4/5':'8536',
#                  '1/6':'8537',
#                  '5/6':'8538',
#                  '1/8':'8539',
#                  '3/8':'8540',
#                  '5/8':'8541',
#                  '7/8':'8541',}

@register.filter
def fractionalize(value):
    f = Fraction(value)
    if f.denominator == f.numerator or f.denominator == 1:
        return value
    else:
        fraction = '<div class="fraction"><span class="numerator">' + str(f.numerator) + '</span>/<span class="denominator">' + str(f.denominator) + '</span></div>'
        return fraction

def day_link(date):
 return "<a href=\"/ohlih/" + date.strftime("%Y/%m/%d") + "\">" + date.strftime("%B %e") + "</a>"

@register.filter
def previous_day(value):
    date = value['list'][0].time.date
    events = Event.objects.filter(time__lt=date).order_by('-time')[:1]
    if len(events)>0:
        return day_link(events[0].time)
    else:
        return ''

@register.filter
def next_day(value):
    date = value['list'][0].time
    events = Event.objects.filter(time__gt=date).order_by('time')
    if len(events)>0:
        return day_link(events[0].time)
    else:
        return ''
    
@register.filter
def hyphenate(value, arg=None, autoescape=None):
    default_dic_path = '/home/ford/sites/ftrain.com/htdocs/ftrain/'
    lang='en_US'
    minlen = 5
    h = hyphenator(lang,directory=default_dic_path)
    new = []
    for word in value.split(u' '):
        if len(word) > minlen and word.isalpha():
            new.append(u'&shy;'.join(h.syllables(word)))
        else:
            new.append(word)
            result = u' '.join(new)
    return  result
hyphenate.needs_autoescape = True
    
