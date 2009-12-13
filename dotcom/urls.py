from django.conf import settings
from os import path
from django.conf.urls.defaults import *
from models import *
import views

urlpatterns = patterns('',
                       # Month page
                       # http://docs.djangoproject.com/en/dev/ref/generic-views/

                       (r'^subject/(?P<subject>[^\/]+)/?$', views.subject),
                       (r'^archive/(?P<year>\d{4})/?$', views.year),
                       (r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/?$', views.month),
                       (r'^', views.homepage),
                       )
