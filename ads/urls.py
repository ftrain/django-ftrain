from django.conf import settings
from django.conf.urls.defaults import *
from models import *
from views import *

urlpatterns = patterns('',
                       (r'^/?$', ads),
                       )
