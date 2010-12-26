# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#import os.path
#from settings import site_media#, site_upload, backup_dir

from blog.views import main_page, note_save_page, user_page, note_safe_delete_page, note_delete_page, note_page, tag_page, tag_cloud_page, search_page

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fsys/', include('fsys.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
    
    
    (r'^$', main_page),                                                 #main
    (r'^user/(\w+)/$', user_page),                                      #user_page
    (r'^save/$', note_save_page),                                   	#note_save_page
    #(r'^vote/$', bookmark_vote_page),                                   #рейтинги
    (r'^tag/([^\s]+)/$', tag_page),                                     #тэги
    (r'^tag/$', tag_cloud_page),                                        #облако тэгов
    (r'^search/$', search_page),                                        #поиск
    #(r'^popular/$', popular_page),                                      #популярные
    
    (r'^note/(\d+)/$', note_page),                                      #страница 1 записи
    
    (r'^safe_delete/$', note_safe_delete_page),                         #безопасное удаление
    (r'^delete/$', note_delete_page),                                   #удаление


   
    
    


   
)
