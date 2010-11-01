# -*- coding: utf-8 -*-
#bookmarks/views
from django.db import models


#-----------------------------------------------------------------------
class Link(models.Model):
    """Ссылка"""
    url = models.URLField(unique=True)
    
    def __unicode__(self):
        return self.url
#-----------------------------------------------------------------------        
        
            
            
from django.contrib.auth.models import User             #работаем со стандартным еханизмом юзеров
#-----------------------------------------------------------------------
class Bookmark(models.Model):
    """Закладка"""
    title = models.CharField(max_length=200)    #Имя
    user = models.ForeignKey(User)              #кто добавил
    link = models.ForeignKey(Link)              #ссылка
    
    def __unicode__(self):
        return self.title
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
class Tag(models.Model):
    """Тэги"""
    name = models.CharField(max_length=64, unique=True) #имя
    bookmarks = models.ManyToManyField(Bookmark)        #ссылки на закладки
    
    def __unicode__(self):
        return self.name
#-----------------------------------------------------------------------
















