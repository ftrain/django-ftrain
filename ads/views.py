from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.conf import settings
from ftrain.ads.models import *

@cache_page(6 * 60)
def ads(request):
    ads = Ad.objects.all().order_by('weight').reverse()
    return render_to_response('ads.js',{'ads':ads})
