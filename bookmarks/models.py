# -*- coding: utf-8 -*-
#bookmarks/views
from django.db import models

class Link(models.Model):
    url = models.URLField(unique=True)
    
    def __unicode__(self):
        return self.url
        
        
            
from django.contrib.auth.models import User
class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    
    def __unicode__(self):
        return self.title

