from django.conf import settings
from django.conf.urls.defaults import *
from models import *
from views import *

urlpatterns = patterns('',
                       (r'^charts/weight_from_(\d{4})-(\d{2})-(\d{2})_to_(\d{4})-(\d{2})-(\d{2})(\d{1})(\d{1}).png$', chart_weight),

                       # Granular event page
                       (r'^(\d{4})/(\d{2})/(\d+)/(\d+)?$', event),

                       # Day page
                       (r'^(\d{4})/(\d{2})/(\d+)/?$', day),

                       # Month page
                       (r'^(\d{4})/(\d{2})/?$', month),

                       # Year page
                       (r'^(\d{4})/?$', year),

                       # Food/exercise page
                       (r'^kcal/(\d+)?$', kcal),

                       # Home page
                       (r'^', homepage),
                       )
