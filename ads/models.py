from django.db import models

# Impressions will show up in stats. No reason to add the load of an
# update to every page view for something like this.

class Ad(models.Model):
    """
    A simple "ad hosting" solution for promoting small buttons and some text.
    """
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    image = models.ImageField(upload_to='ads')
    url = models.URLField()
    html = models.TextField()
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.name)    
    
class Click(models.Model):
    ad = models.ForeignKey(Ad)
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(date) + str(self.ad)    


