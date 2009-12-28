import datetime

from django.db import models
from imagekit.models import ImageModel
#from batch_select.models import BatchManager

MODEL_FULL_NAME='One Huge Lesson in Humility'

class EventType(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return str(self.name)

class Event(models.Model):
    """
    Our basic unit of time.
    """
    # Comment to load fixtures; then uncomment to migrate
    event_name = models.ForeignKey(EventType)
    time = models.DateTimeField()
    # Comment after running 0006
    # event_type = models.CharField(max_length=100)
    commentary = models.TextField(blank=True)

#    objects = BatchManager()

    class Meta:
        ordering = ['-time']
        verbose_name = "Event"
        get_latest_by = 'time'

    class Admin:
        date_hierarchy = 'time'

    def __unicode__(self):
        return str(self.time) + " - " + self.event_name.name

class Energy(models.Model):
    name = models.CharField(max_length=255)
    kcal = models.IntegerField()
    kcal_is_est = models.BooleanField()    

#   objects = models.Manager()
#    reversemanager = ReverseManager({'consumptions':'consumption_set',})

    class Meta:
        ordering = ['name']
        verbose_name = "Sources and utilizers of energy"
        verbose_name_plural = "Sources and utilizers of energy"

#    objects = BatchManager()

    def __unicode__(self):
        return self.name[:40] + ' (' + str(self.kcal) + ' cal.)'

    display = __unicode__

class Consumption(models.Model):
    in_event = models.ForeignKey(Event)
    of_energy = models.ForeignKey(Energy)
    order = models.IntegerField(null=True,blank=True)
    quantity = models.CharField(max_length=10)   

    class Meta:
        ordering = ['order','of_energy']
        verbose_name = "Utilization"

#    objects = BatchManager()

    def __unicode__(self):
        return self.of_energy.name + '/' + str(self.quantity)

class BloodPressure(models.Model):
    in_event = models.ForeignKey(Event)
    systolic = models.IntegerField()
    diastolic = models.IntegerField()

#    objects = BatchManager()

    def __unicode__(self):
        return str(self.systolic) + '/' + str(self.diastolic)

class Weight(models.Model):
    in_event = models.ForeignKey(Event)
    weight = models.FloatField()

    class Meta:
        ordering = ['-in_event']

#    objects = BatchManager()

    def __unicode__(self):
        return str(self.in_event.time) + ': ' + str(self.weight)

class Image(ImageModel):
    in_event = models.ForeignKey(Event, null=True)
    order = models.IntegerField(null=True,blank=True,default=100)
    name = models.CharField(max_length=100,default='[untitled]')
    original_image = models.ImageField(upload_to='photos')
    cache_filename_format = "image/%(specname)s/%(filename)s.%(extension)s"

#    objects = BatchManager()
    
    class IKOptions:
        spec_module = 'kcal.specs'
        cache_dir = 'photos'
        image_field = 'original_image'
        save_count_as = 'num_views'

    def __unicode__(self):
        return self.name
