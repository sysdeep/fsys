# -*- coding: utf-8 -*-
#blog/models
from django.db import models


#-----------------------------------------------------------------------
#class Link(models.Model):
#    """Ссылка"""
#    url = models.URLField(unique=True)
    
#    def __unicode__(self):
#        return self.url
#-----------------------------------------------------------------------        
        
            
            
from django.contrib.auth.models import User             #работаем со стандартным еханизмом юзеров
#-----------------------------------------------------------------------
class Note(models.Model):
    """Запись"""
    title = models.CharField(max_length=200)    #Имя
    desc = models.TextField()					#тело записи
    user = models.ForeignKey(User)              #кто добавил
    time_c = models.DateTimeField(auto_now_add=True)				#время создания
    #link = models.ForeignKey(Link)              #ссылка
    
    def __unicode__(self):
        return self.title
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
class Tag(models.Model):
    """Тэги"""
    name = models.CharField(max_length=64, unique=True) #имя
    notes = models.ManyToManyField(Note)        		#ссылки на запись
    
    def __unicode__(self):
        return self.name
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
class SharedNote(models.Model):
    """Расшаривание и рейтинг"""
    
    note = models.ForeignKey(Note, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(User)
    
    def __unicode__(self):
        return u'%s, %s' % (self.note, self.votes)
#-----------------------------------------------------------------------















