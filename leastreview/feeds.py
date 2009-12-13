from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from models import Event

class LilliputEventsFeed(Feed):
    title = "The Lilliput Review, by Paul Ford"
    link = "http://www.lilliputreview.com"
    subtitle = "Big fella, little reviews."
    author_name = "Paul Ford"
    item_author_name = "Paul Ford"
    item_author_email = "ford@ftrain.com"
    item_author_link = "http://www.ftrain.com"
    item_copyright = 'Copyright (c) Paul Ford'
    feed_guid = 'http://www.ftrain.com/ftrain/feeds/the-lilliput-review/'

    feed_type = feedgenerator.Atom1Feed

    def items(self):
        return Event.objects.order_by('-time')[:25].select_related()

    def item_link(self, obj):
        return 'http://www.lilliputreview.com/lilliput/' + str(obj.time.strftime("%Y/%m/%d")) + '#' + obj.time.strftime("%H:%M")

    def item_pubdate(self, item):
        return item.time
