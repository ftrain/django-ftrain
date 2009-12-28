from django.conf.urls.defaults import *

#-------------------------------------------------------------------------------
# Feeds
#-------------------------------------------------------------------------------

from ftrain.kcal.feeds import KcalEventsFeed
from ftrain.kcal.feeds import KcalDaysFeed
# from ftrain.radio.feeds import MaryislaughingPostsFeed
# from ftrain.reviews.feeds import LeastreviewReviewsFeed
# from ftrain.dotcom.feeds import FtrainCompleteFeed

urlpatterns = patterns('',)

#-------------------------------------------------------------------------------
# Admin
#-------------------------------------------------------------------------------

from django.contrib import admin
admin.autodiscover()

urlpatterns = urlpatterns + patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/Users/ford/sites/ftrain.com/htdocs/m/'}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': {'ohlih-events': KcalEventsFeed, 'ohlih-days': KcalDaysFeed}}),
    )

#-------------------------------------------------------------------------------
# Search
#-------------------------------------------------------------------------------

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
#from ftrain.haystack.views import FtrainFacetedSearchView

#sqs = SearchQuerySet().facet('type').facet('month').facet('site')
sqs = SearchQuerySet().facet('title')

urlpatterns = urlpatterns + patterns(
    '',
    # (r'^search/', include('haystack.urls')),
    url(r'^search/', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    # reload_all=False
)

#-------------------------------------------------------------------------------
# Sites    
#-------------------------------------------------------------------------------

urlpatterns = urlpatterns + patterns('',
    # Ftrain
    (r'^dotcom/', include('ftrain.dotcom.urls')),

    # One Huge Lesson in Humility
    (r'^ohlih/', include('ftrain.kcal.urls')),

    # Mary is Laughing
    (r'^mary-is-laughing/', include('ftrain.radio.urls')),

    # Least Review
    (r'^least-review/', include('ftrain.reviews.urls')),

    # "Advertising" server
    (r'^ads/', include('ftrain.ads.urls')),

    # Featurism
    (r'^featurism/', include('ftrain.features.urls')),
  
)
