from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from models import Event

class KcalEventsFeed(Feed):
    title = "One Huge Lesson in Humility, by Myself (Events)"
    link = "http://www.ohlih.com"
    subtitle = "Making the navel harder to gaze upon."
    author_name = "Paul Ford"
    item_author_name = "Paul Ford"
    item_author_email = "ford@ftrain.com"
    item_author_link = "http://www.ftrain.com"
    item_copyright = 'Copyright (c) Paul Ford'
    feed_guid = 'http://www.ftrain.com/ftrain/feeds/ohlih-events/'

    feed_type = feedgenerator.Atom1Feed
        
    def items(self):
        return Event.objects.order_by('-time')[:25].select_related()

    def item_link(self, obj):
        return 'http://www.ohlih.com/ohlih/' + str(obj.time.strftime("%Y/%m/%d")) + '#' + obj.time.strftime("%H:%M")

    def item_pubdate(self, item):
        return item.time

class KcalDaysFeed(Feed):
    title = "One Huge Lesson in Humility, by Myself (Days)"
    link = "http://www.ohlih.com"
    subtitle = "Making the navel harder to gaze upon."
    author_name = "Paul Ford"
    item_author_name = "Paul Ford"
    item_author_email = "ford@ftrain.com"
    item_author_link = "http://www.ftrain.com"
    item_copyright = 'Copyright (c) Paul Ford'
    feed_guid = 'http://www.ftrain.com/ftrain/feeds/ohlih-events/'

    feed_type = feedgenerator.Atom1Feed

    def items(self):
        return Event.objects.order_by('-time')[:25].select_related()

    def item_link(self, obj):
        return 'http://www.ohlih.com/ohlih/' + str(obj.time.strftime("%Y/%m/%d")) + '#' + obj.time.strftime("%H:%M")

    def item_pubdate(self, item):
        return item.time
