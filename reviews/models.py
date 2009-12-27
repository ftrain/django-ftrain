from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageModel

class Review(models.Model):
    of_thing = models.ForeignKey('Thing', null=True)
    time = models.DateTimeField()
    box = models.TextField(blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField(max_length=2)
    author = models.ForeignKey(User, blank=True, null=True)
    count = models.IntegerField(max_length=4)

    def __unicode__(self):
        return str(self.of_thing.name) + ' Review'

class Thing(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey('Type', null=True)
    parent_thing = models.ForeignKey('Thing',blank=True,null=True)

    def __unicode__(self):
        return str(self.name)

class Type(models.Model):
    name = models.CharField(max_length=255)
    parent_type = models.ForeignKey('Type', null=True,blank=True)
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return str(self.name)

class Image(ImageModel):
    of_thing = models.ForeignKey(Thing, null=True)
    order = models.IntegerField(null=True,blank=True,default=100)
    name = models.CharField(max_length=100,default='[untitled]')
    original_image = models.ImageField(upload_to='leastreview')
    cache_filename_format = "image/%(specname)s/%(filename)s.%(extension)s"
    
    class IKOptions:
        spec_module = 'ftrain.leastreview.specs'
        cache_dir = 'photos'
        image_field = 'original_image'
        save_count_as = 'num_views'

    def __unicode__(self):
        return self.name
