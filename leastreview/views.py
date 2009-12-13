import time
from datetime import date
from fractions import Fraction
import numpy as numpy

import re

from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.conf import settings

from models import *

@cache_page(20)
def homepage(request):
    events = Event.objects.all().order_by('time').reverse()[:15]
    return render_to_response('homepage.html',{'events':events})

def event(request, year, month, event):
    pass

def kcal(request, kcal):
    name = Energy.objects.filter(id=kcal)
    events = Event.objects.filter(consumption__of_energy__id=kcal).order_by('time').reverse()
    return render_to_response('kcal.html',{'events':events,'name':name})

@cache_page(60 * 5)
def detail(request, year, month, day):
    events = Event.objects.filter(time__year=year).filter(time__month=month).filter(time__day=day).select_related()
    return render_to_response('day.html',{'events':events})

def extract_image(text):
    image = {}
    matches = re.findall(r'\((.+)/([^/]+).(jpg|jpeg|gif|png)', text, re.IGNORECASE|re.UNICODE)
    if len(matches) and len(matches[0]) > 1:
        image = {'url':matches[0][0], 'image':matches[0][1], 'suffix':matches[0][2]}
    return image

#@cache_page(60 * 5)
def month(request, year, month):
    month_val = date(int(year), int(month), 1)
    events = Event.objects.filter(time__year=year).filter(time__month=month).order_by('time').select_related()
    days = {}

    # Make day dict
    for event in events:
        day_key = str(event.time.day)

        for food in event.consumption_set.all():
            val = int(float(food.of_energy.kcal) * float(Fraction(food.quantity)))
            if day_key not in days:
                days[day_key]={}
                days[day_key]['image']= event.image_set.all()
                days[day_key]['day'] = int(day_key)
                days[day_key]['day_time'] = event.time
                days[day_key]['events'] = []
            days[day_key]['events'].append(val)

    #Organize an array of dicts
    new_days = []
    day_keys = days.keys()
    day_keys.sort()

    for day_key in day_keys:
        nd = {}
        nd['day'] = days[day_key]['day']
        nd['image'] = days[day_key]['image']
        nd['day_time'] = days[day_key]['day_time']
        cal_list = days[day_key]['events']
        nd['input'] = sum(filter(lambda x: x > 0, cal_list))
        nd['output'] = sum(filter(lambda x: x < 0, cal_list))
        nd['combined'] = sum(cal_list)
        new_days.append(nd)

    good = {'input':{}, 
            'output':{}, 
            'combined':{}, 
            }

    good['total_days'] = len(new_days)


    good['input']['days'] = len(filter(lambda x: x < settings.TOTAL_ALLOWED_CALORIES, map(lambda x: x['input'], new_days)))
    good['input']['percent'] = int(100 * good['input']['days']/good['total_days'])

    good['output']['days'] = len(filter(lambda x: x < 0, map(lambda x: x['output'], new_days)))
    good['output']['percent'] = int(100 * good['output']['days']/good['total_days'])

    good['combined']['days'] = len(filter(lambda x: x < settings.TOTAL_ALLOWED_CALORIES, map(lambda x: x['combined'], new_days)))
    good['combined']['percent'] = int(100 * good['combined']['days']/good['total_days'])

    #Calculate sum, median, and mean
    month_data = { 'sum':{}, 'median':{}, 'mean':{}, 'name':month_val}
    for field in ['input', 'output', 'combined']:

        l = map(lambda x: x[field], new_days)
        month_data['sum'][field] = sum(l)
        month_data['mean'][field] = int(numpy.mean(l))
        month_data['median'][field] = int(numpy.median(l))

    return render_to_response('month.html',{'days':new_days,
                                            'month':month_data,
                                            'good':good,
                                            'max_cals':settings.TOTAL_ALLOWED_CALORIES,
                                            })

