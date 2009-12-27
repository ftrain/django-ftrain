import re

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.forms import formsets
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import serializers

from models import *

import mary
import sys



# Create your views here.

def home(request):
    results={
        'results': Post.objects.reverse().order_by('publish')[:10], 
        'MEDIA_URL':mary.settings.MEDIA_URL,
        }
    
    return render_to_response('home.html', results)
