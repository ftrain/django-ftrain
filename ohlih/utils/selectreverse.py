"""
django-selectreverse

Custom manager to reduce sql queries for m2m and reverse fk relationships

"""

from django.db import models
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor,  ReverseManyRelatedObjectsDescriptor,  ManyRelatedObjectsDescriptor
from django.core.exceptions import ImproperlyConfigured

class ReverseManager(models.Manager):
    """
    manager that allows you to pass in a dict, declaring a set of reverse relationships, matched to
    an attributename.
    If you use this manager to fetch the items,
    the related items of the reverse relationship will be prefetched into a list for each object
    made available as an attribute of the object.

    """
    def __init__(self, reversemapping=None):
        self.reversemapping = reversemapping or {}
        super(ReverseManager, self).__init__()

    def select_reverse(self,  reversemapping=None):
        reversemapping = reversemapping or self.reversemapping
        return self.get_query_set(reversemapping)

    def get_query_set(self, reversemapping=None):
        reversemapping = reversemapping or self.reversemapping
        return ReverseQuerySet(model=self.model, reversemapping=reversemapping)

class ReverseQuerySet(models.query.QuerySet):
    def __init__(self, model=None, query=None, reversemapping=None):
        self.reversemapping = reversemapping or {}
        super(ReverseQuerySet, self).__init__(model, query)

    def _clone(self, klass=None, setup=False, **kwargs):
        c = super(ReverseQuerySet, self)._clone(klass=klass, setup=setup, **kwargs)
        c.reversemapping = self.reversemapping
        return c

    def select_reverse(self, reversemapping=None):
        if reversemapping:
            q = self._clone()
            q.reversemapping = reversemapping
        return q

    def _fill_cache(self, num=None):
        super(ReverseQuerySet, self)._fill_cache(num)
        reversemapping = self.reversemapping or {}
        ids = [item.pk for item in self._result_cache]
        target_maps = {}
        for k, v in reversemapping.iteritems():
            if hasattr(self.model,  k):
                raise ImproperlyConfigured,  "Model %s already has an attribute %s" % (self.model,  k)
        for k, v in reversemapping.iteritems():
            target_map= {}
            descriptor = getattr(self.model,  v)
            if isinstance(descriptor, ForeignRelatedObjectsDescriptor):
                rel = getattr(self.model, v).related
                for item in rel.model.objects.filter(**{rel.field.name+'__in':ids}).all():
                    target_map.setdefault(getattr(item, rel.field.get_attname()), []).append(item)
                target_maps[k]=target_map
            elif isinstance(descriptor, ReverseManyRelatedObjectsDescriptor):
                field = getattr(self.model, v).field
                for item in field.rel.to.objects.filter(**{self.model.__name__.lower() +'__in':ids}).all().extra( \
                            select={'main_id': field.m2m_db_table() + '.' + field.m2m_column_name()}):
                    target_map.setdefault(getattr(item, 'main_id'), []).append(item)
                target_maps[k]=target_map
            elif isinstance(descriptor, ManyRelatedObjectsDescriptor):
                rel = getattr(self.model, v).related
                for item in rel.model.objects.filter(**{rel.field.name +'__in':ids}).all().extra( \
                            select={'main_id': rel.field.m2m_db_table() + '.' + rel.field.m2m_column_name()}):
                    target_map.setdefault(getattr(item, 'main_id'), []).append(item)
                target_maps[k]=target_map
            else:
                raise ImproperlyConfigured, "Unsupported mapping %s %s" % (v, descriptor)

        for item in self._result_cache:
            for k, v in reversemapping.iteritems():
                setattr(item, k, target_maps[k].get(item.pk,[]))



