from django.db import models
from django.conf import settings
from datetime import datetime
import time, random
import xml.etree.ElementTree as ET

import ftrain.dotcom.models
from ftrain.dotcom.models import Person, Post, Link, By


site = ET.parse('out.xml')
people = site.findall("//person")
people_dict = {}

print "Deleting old people"
try:
    for todel in Person.objects.all():
        todel.delete()
except Exception as e:
    print "Does not exist..."

print "Deleting old posts"
try:
    for todel in Post.objects.all():
        todel.delete()
except Exception as e:
    print "Does not exist..."

for p in people:
    new = Person()
    new.slug = p.findtext('slug')
    title = p.findtext('title')
    if title:
        new.title = p.findtext('title')
    else:
        new.title = '[Untitled]'
    print "Saving " + new.slug
    new.save()
    people_dict[new.slug] = new

post_dict = {}
posts = site.findall("//arb")

for p in posts:
    new = Post()
    slug = p.findtext('slug')
    if slug:
        new.slug = slug
        print "Saving " + new.slug
        # '2000-11-01 00:00:00'
        date = p.findtext('publish')
        els = date.split('-')
        els[2] = els[2][0:2]
        print els
        publish = datetime(int(els[0]),int(els[1]),int(els[2]))
        new.publish = publish
        title = p.findtext('title')
        if title:
            new.title = title
        else:
            new.title = '[Untitled]'
        description = p.findtext('description')
        if description:
            new.description = description
        if p.find('text'):
            els_as_text = map(lambda el: ET.tostring(el), p.find('text')._children)
            new.text = "\n".join(els_as_text)
        new.save()
        post_dict[new.slug] = new

        for author in p.findall('author'):
            if author:
                a = author.text
                print "Author:" + a
                if a:
                    person = people_dict[author.text]
                    by = By()
                    by.author = person
                    by.item = new
                    by.save()
                    
# Now run through once more and add in parent relationships.

for p in posts:
    child = p.findtext('slug')
    if child:
        post = post_dict[child]
        parent = p.find('parent').text
        if parent and post_dict.has_key(parent):
            post.parent = post_dict[parent]
            print "Parent = " + parent + "; child = " + child
            post.save()
    

