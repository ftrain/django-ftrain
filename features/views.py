from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from ftrain.featurism.models import *
from datetime import datetime

@cache_page(60)
def homepage(request):
    events = Product.objects.all().order_by('time')[:60]
    return render_to_response('homepage.html',{'events':events})

@cache_page(60 * 15)
def detail(request, year, month, day):
    events = Product.objects.filter(time__year=year).filter(time__month=month).filter(time__day=day)
    return render_to_response('homepage.html',{'events':events})
