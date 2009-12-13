from haystack import indexes
from haystack import site
import datetime

from ohlih.models import Event
import ohlih.models as ohlih

class EventIndex(indexes.SearchIndex):
#    site = indexes.CharField(ohlih.MODEL_FULL_NAME)
    title = indexes.CharField(model_attr='event_name')
    time = indexes.DateTimeField(model_attr='time')
    text = indexes.CharField(model_attr='commentary',document=True)
#    parents = indexes.MultiValue
#    children = indexes.MultiValue
    text_cache = indexes.CharField(use_template=True,indexed=False)
# month = indexes.DateTimeField(Y-M-01)

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Event.objects.filter(time__lte=datetime.datetime.now())

site.register(Event, EventIndex)
