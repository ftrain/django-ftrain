# Utilities
import time
import datetime
from datetime import date
from fractions import Fraction
import numpy as numpy
import re
import logging

# Django

from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.conf import settings
import django.http

# Charts
import matplotlib
import matplotlib.axes

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import itertools
# Me

from models import *

@cache_page(30)
def homepage(request):
    events = Event.objects.all().order_by('time').reverse()[:15]
    return render_to_response('homepage.html',{'events':events,})

def event(request, year, month, event):
    pass

@cache_page(60 * 5)
def kcal(request, kcal):
    name = Energy.objects.filter(id=kcal)
    events = Event.objects.filter(consumption__of_energy__id=kcal).order_by('time').reverse()
    return render_to_response('kcal.html',{'events':events,'name':name})

@cache_page(60 * 5)
def day(request, year, month, day):
    events = Event.objects.filter(time__year=year).filter(time__month=month).filter(time__day=day).select_related()
    return render_to_response('day.html',{'events':events})
        
@cache_page(60*60*24)
def year(request, year):
    year = Event.objects.filter(time__year=year).select_related()

    return render_to_response('year.html',{'years':year})


 
@cache_page(60 * 5)
# I AM THE WRONG WAY TO SOLVE THIS PROBLEM AND SHOULD BE MANY SMALLER FUNCTIONS
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



@cache_page(60 * 60 * 24)
def chart_weight(request, fy, fm, fd, ty, tm, td, annotate_begin, annotate_end, width=1.9, height=0.4):
    
    from_date = datetime.date(int(fy),int(fm),int(fd))
    to_date = datetime.date(int(ty),int(tm),int(td))
    
    # Get all events that have weights between (and including)
    # from_date and to_date
    weights = Event.objects.filter(time__gte=from_date).filter(time__lte=to_date).filter(weight__isnull=False).order_by('time').select_related('weight')

    # Now let's pile in some data
    x=[]
    y=[]
    for event in weights:
        date = event.time.date()
        weight = event.weight_set.all()[0].weight
        x.append(date)
        y.append(weight)

    # Set up the chart; we use 100 DPI because it makes
    # pixel-math easy

    matplotlib.rc('lines', linewidth=1, color='black')
    matplotlib.rc('font', size=6)

    fig=Figure(dpi=100,frameon=False)
    fig.set_figwidth(width)
    fig.set_figheight(height)

    ax=fig.add_subplot(111,
                       autoscale_on=True,
                       frameon=False,
                       yticklabels=[],
                       xticklabels=[])

    ax.plot_date(x, y, '-')

    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')


    # Add the date to the beginning
    if annotate_begin == '1':
        ax.annotate(x[0].strftime("%b %e") + '/' + str(int(y[0])) + '', 
                    xy=(18, -40),
                    xycoords='figure pixels',
                    arrowprops=None, 
                    color='black')


    # And the weight to the end (because we tend to know what day it
    # is from the rest of the site)

    if annotate_end == '1':
        ax.annotate(str(int(y[-1])),
                    xy=(160, -25),
                    xycoords='figure pixels',
                    arrowprops=None, 
                    color='black')
        
    canvas = FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    
    return response
