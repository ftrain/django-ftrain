from django import template
from fractions import Fraction
from hyphen import hyphenator, dictools, config
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.conf import settings
import numpy as numpy
import datetime

from kcal.models import Event

import re
import os

register = template.Library()
@register.filter
def sum_calories(set_of_foods):
    "Sums calories of a given meal"
    sum = 0
    for food in set_of_foods:
        sum = sum + int(float(food.of_energy.kcal) 
                        * float(Fraction(food.quantity)))
    return sum

@register.filter
def sum_daily_calories(day_list):
    "Sums calories of a given day"
    sum = 0
    rsum = 0
    for event in day_list:
        for food in event.consumption_set.all():
            sum = sum + int(float(food.of_energy.kcal) 
                            * float(Fraction(food.quantity)))
            if food.of_energy.kcal > 0:
                rsum = rsum + int(float(food.of_energy.kcal) 
                                  * float(Fraction(food.quantity)))                
    return [sum, rsum]

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
    num = ''.join(parts)
    num = re.sub(r'\-(.*)',r'<span class="neg"><span class="minus">&#8722;</span>\1</span>',num)
    return num

@register.filter
def smartypants(value):
    try:
        import smartypants
        return smartypants.smartyPants(value)
    except:
        return value    

@register.filter
def strip_paras(value):
    """
    Removes <p> tags from strings.

    >>> strip_paras("<p>test</p>")
    'test'
    """
    return re.sub(r'<p>(.*)</p>',r'\1',value)

@register.filter
def fix_type_pre(value):
    """
    So far this only modifies ellipses.

    >>> fix_type_pre("... ....")
    ' <nobr> . . . </nobr>   <nobr> . . . . </nobr> '
    """
    new_value = value
    new_value = re.sub(r'\.{3}[^\.]',r' <nobr> . . . </nobr> ', new_value)
    new_value = re.sub(r'\.{4}',r' <nobr> . . . . </nobr> ', new_value)
    return new_value

@register.filter
def fix_type_post(value):
    new_value = value
#    new_value = re.sub(r'\&amp;',r'<i>&amp;</i>', new_value)
#    new_value = re.sub(r'\Wand\W',r' <i>&amp;</i> ', new_value)
    new_value = re.sub(r'\Wetc\.',r' <i>&amp;</i>c. ', new_value)
    new_value = re.sub(r'([\d\s])(oz|fl\. oz|c|pt|qt|gal|in|ft|yd|m|hr|min|tsp|tbsp)\.',r'\1<i>\2</i>.', new_value)
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
    """
    Return some HTML when given a fraction.
    """
    f = Fraction(value)
    if f.denominator == f.numerator or f.denominator == 1:
        return value
    else:
        fraction = '<div class="fraction"><span class="numerator">' \
            + str(f.numerator) \
            + '</span>/<span class="denominator">' \
            + str(f.denominator) \
            + '</span></div>'
        return fraction

def day_link(date):
 return "<a href=\"/ohlih/" + date.strftime("%Y/%m/%d") + "\">" + date.strftime("%b %e") + "</a>"

@register.filter
def previous_day(value):
    """
    Give us a link to the previous day
    """
    date = value['list'][0].time.date
    events = Event.objects.filter(time__lt=date).order_by('-time')[:1]
    if len(events)>0:
        return '&lt;' + day_link(events[0].time)
    else:
        return ''

@register.filter
def next_day(value):
    """
    Give us a link to the next day
    """
    date = value['list'][0].time
    events = Event.objects.filter(time__gt=date).order_by('time')
    if len(events)>0:
        return day_link(events[0].time) + '&gt;'
    else:
        return ''
    
@register.filter
def remaining(value):
    return settings.TOTAL_ALLOWED_CALORIES - value
    
@register.filter
def hyphenate(value, arg=None, autoescape=None):
    lang='en_US'
    minlen = 5
    h = hyphenator(lang,directory=settings.DEFAULT_DIC_PATH)
    new = []
    for word in value.split(u' '):
        if len(word) > minlen and word.isalpha():
            new.append(u'&shy;'.join(h.syllables(word)))
        else:
            new.append(word)
            result = u' '.join(new)
    return  result
hyphenate.needs_autoescape = True

def calorie_list(list_of_events):
    """
    Get a simple list of calories out of a list of events
    """
    the_list = []
    for e in list_of_events:
        val = 0
        for food in e.consumption_set.all():
            val += int(float(food.of_energy.kcal) \
                           * float(Fraction(food.quantity)))
        the_list.append(val)
    return the_list

def calorie_list_days(list_of_days):
    """
    Get a simple list of calories out of a list of days (thus summing
    the calories in each event)
    """
    the_list = []
    for day in list_of_days:
        all_cals = calorie_list(day['list'])
        cals_filtered = filter(lambda x: x>0, all_cals)
        val = numpy.sum(cals_filtered)
        the_list.append(val)
    return the_list

def extract_info(cal_list):
    """
    Take a list of calories.
    """
    dict = {}
    dict['cal_list'] = cal_list
    dict['sum'] = numpy.sum(cal_list)
    dict['median'] = numpy.median(cal_list)
    dict['mean'] = int(numpy.mean(cal_list))
    dict['min'] = numpy.min(cal_list)
    dict['max'] = numpy.max(cal_list)
    return [dict]
            
@register.filter
def process_events(list_of_events):
    return extract_info(calorie_list(list_of_events))

@register.filter
def process_days(list_of_days):
    calorie_list = calorie_list_days(list_of_days)
    days = extract_info(calorie_list)
    return days

@register.filter
def last_month(a_month):
    "Subtracts a duration of 1 month"
    return a_month - datetime.timedelta(weeks=4)

@register.filter
def weight_lost(list_of_days):
    diff = 0
    weights = []
    for day in list_of_days:
        for event in day['list']:
            ws = event.weight_set.all()
            if len(ws):
                weights.append(ws[0].weight)
    diff = weights[len(weights)-1] - weights[0]
    return diff

@register.filter
def to_date(date):
    y=int(date[0:4])
    m=int(date[5:7])
    d=int(date[8:10])
    return datetime.date(y,m,d)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

