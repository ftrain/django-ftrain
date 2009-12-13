from haystack import indexes
from haystack import site
import datetime

from dotcom.models import Post
import dotcom.models as dotcom

class PostIndex(indexes.SearchIndex):
    title = indexes.CharField(model_attr='title')
    time = indexes.DateTimeField(model_attr='publish')
#    time = indexes.DateTimeField(model_attr='publish')
    text = indexes.CharField(model_attr='text',document=True)
    text_cache = indexes.CharField(use_template=True,indexed=False)

    def prepare_time(self, obj):
        return "%s <%s>" % (obj.user.get_full_name(), obj.user.email)

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.filter(publish__lte=datetime.datetime.now())

site.register(Post, PostIndex)
