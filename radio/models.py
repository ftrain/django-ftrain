from django.db import models
from django.contrib.auth.models import User

# Create your models here.
   
class Show(models.Model):
    show_name = models.CharField(max_length=255,default="The Jack Benny Program")
    show_title = models.CharField(max_length=255,blank=True)
    file_link = models.URLField(blank=True)
    embeddable = models.BooleanField()
    file_link_note = models.CharField(max_length=255,blank=True)
    airdate = models.DateField(blank=True)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return self.show_title + " (" + str(self.airdate) + ")"

class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    publish = models.DateTimeField(blank=False)
    draft = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    related_shows = models.ManyToManyField(Show)
    author = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.show_title + " (" + str(self.originally) + ")"
