from django.db import models
from django.conf import settings
from datetime import datetime
import time, random

# Adapted from the custom XSLT Ftrain.com, written from 1998-2005.

# This is not promoted as the right, or even a good, way to program a
# CMS--it's a distillation of custom code in Perl, PHP, and XSLT/Java,
# over ten years, seeking to find a compromise between the arbitrary
# nature of RDF/triples where everything is metadata capable of
# interconnection and the convenience of web-based editing in a
# relational model, where some data is privileged as the "real" data
# for the convenience of all.

# And the author is in many ways still an amateur. This data model is
# more organized around his needs; it's assumed that the system will
# convert the data to something useful for the reader; in this case by
# feeding it into SOLR and making it easily searchable.


#-------------------------------------------------------------------------------
# Arbs
#-------------------------------------------------------------------------------

class Arb(models.Model):
    """
    An arb is an ARBitrary publishing unit for a website--dates, some
    text, a parent relationship. And a title, although that's
    metadata. It's so often there that w hen it's not that's the
    exception that proves the rule. Plus it leads to consistency in
    the admin interface to have a title.
    """

    created = models.DateTimeField(default=datetime.now)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=255)    

    def __unicode__(self):
        return self.title + " (Arb)"

class Item(Arb):
    """
    An item is the root form (an article or post or link--a thing that
    is itself). We don't say what _type_ of thing an item is; we count
    on the object to do that for us.
    """
    publish = models.DateTimeField(default=datetime.now)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    parent = models.ForeignKey("Arb",related_name="arb_parent",blank=True,null=True)

    def __unicode__(self):
        return self.title + ' (Item)'

class Post(Item):
    """
    A Post is an Item that can be either live or not, and can reside
    on the front page or not. And has a subtitle.
    """
    live = models.BooleanField(default=True)
    front_page = models.BooleanField(default=True)
    subtitle = models.CharField(max_length=255,blank=True)    

    def __unicode__(self):
        return self.title + ' (Post)'

#   In addition to Post we may want to eventually have essays, jokes,
#   slideshows, photos, etc. They can all have large and arbitrary
#   data structures, or be apps unto themselves.

class Link(Arb):
    """
    A link is an arb of convenience--useful for a quick one-off
    sideblog. It's assumed that data will be tugged out of the code
    rather than put in via tags, which can get too complicated too
    quickly.

    It's halfway between an Item and a Thing.
    """
    # The link can get parsed into the text; otherwise it will cover the entire section.
    href = models.URLField(blank=True, max_length=300)

    # We may cache RSS and Twitter feeds; this way we can compare to
    # old feed data to make sure we don't duplicate items.
    identifier = models.CharField(max_length=255)    

    def __unicode__(self):
        return "Link " + self.text

#-------------------------------------------------------------------------------
# Things
#-------------------------------------------------------------------------------

class Thing(Arb):
    """
    A Thing is an arb that represents something. Like a tag, or a
    place. A Thing, cast as a Place, might be "China." An Item called
    "China" would be about China; a Thing called "China" would be an
    identifier to represent China.

    We care about Authors, and Places, for instance.
    """
    slug = models.SlugField()
    # We may want to have a different version of the title for sorting
    title_sort = models.CharField(max_length=255, blank=True)    
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title + '(Thing)'

class Person(Thing):
    """
    People, usually people who write things
    """
    def __unicode__(self):
        return self.title + '(Person)'


#-------------------------------------------------------------------------------
# Relationships
#-------------------------------------------------------------------------------

class Relationship(models.Model):
    """
    We use relationships to relate Arbs, most particularly Things and Items
    """
    def __unicode__(self):
        return "Relationship: " + self.title

class By(Relationship):
    item =  models.ForeignKey("Item")
    author =  models.ForeignKey("Person")

    def __unicode__(self):
        return self.item.title + " BY " + self.author.title

class SeeAlso(Relationship):
    from_arb =  models.ForeignKey("Arb",related_name="from")
    to_arb =  models.ForeignKey("Arb",related_name="to")

    def __unicode__(self):
        return "See Also: " + self.to_arb

