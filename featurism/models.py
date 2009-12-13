from django.db import models
from django.contrib import admin

class Type(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self',blank=True,null=True)

    def __unicode__(self):
        return str(self.name)

class Environment(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self',blank=True,null=True)

    def __unicode__(self):
        return str(self.name)

class Product(models.Model):
    created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    has_type = models.ManyToManyField(Type)
    has_environment = models.ManyToManyField(Environment)
    parent = models.ForeignKey('self',blank=True,null=True)
    def __unicode__(self):
        return str(self.name)

class Version(models.Model):
    of_product = models.ForeignKey('Product')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return str(self.of_product) + " v." + str(self.name) 

class Feature(models.Model):
    of_version = models.ForeignKey('Version')
    order = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self',blank=True,null=True)

    def __unicode__(self):
        return '%s: %s' % (self.of_version, self.name)

class Commentary(models.Model):
    on_feature = models.ForeignKey('Feature')
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.in_feature, self.title)

class FeatureAdmin(admin.ModelAdmin):
    search_fields = ('name','description',)
    fieldsets = (
        (None, {
            'fields': ('order','name','description',)
        }),
    )

class FeatureInline(admin.TabularInline):
    model = Feature

