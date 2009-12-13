# Utilities
import time
import datetime

# Django

from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.conf import settings
import django.http

# Me

from ftrain.dotcom.models import *

#@cache_page(30)
def homepage(request):
    posts = Post.objects.all().order_by('publish').reverse()[:10]
    return render_to_response('dotcom.html',{'posts':posts,})

@cache_page(30)
def subject(request, subject):
    posts = Post.objects.all().filter(publish__year=year).filter(publish__month=month).order_by('publish')
    return render_to_response('month.html',{'posts':posts,})

@cache_page(30)
def month(request, year, month):
    posts = Post.objects.all().filter(publish__year=year).filter(publish__month=month).order_by('publish')
    return render_to_response('month.html',{'posts':posts,})

@cache_page(30)
def year(request, year):
    posts = Post.objects.all().filter(publish__year=year).filter(publish__month=month).order_by('publish')
    return render_to_response('month.html',{'posts':posts,})

@cache_page(3600 * 24)
def javascript(request):
    posts = Post.objects.all().order_by('publish')
    return render_to_response('monthsJs.html',{'posts':posts,})
