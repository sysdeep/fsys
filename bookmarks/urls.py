# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#import os.path
#from settings import site_media#, site_upload, backup_dir

from bookmarks.views import main_page, user_page, bookmark_save_page, tag_page, tag_cloud_page, search_page, bookmark_vote_page, popular_page, bookmark_page

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
    (r'^save/$', bookmark_save_page),                                   #bookmark_save_page
    (r'^vote/$', bookmark_vote_page),                                   #рейтинги
    (r'^tag/([^\s]+)/$', tag_page),                                     #тэги
    (r'^tag/$', tag_cloud_page),                                        #облако тэгов
    (r'^search/$', search_page),                                        #поиск
    (r'^popular/$', popular_page),                                      #популярные
    
    (r'^bookmark/(\d+)/$', bookmark_page),



   
    
    


    #(r'^about/', direct_to_template, {'template': 'about/about_page.html'}),  #about
    #(r'^about_news/', direct_to_template, {'template': 'about/about_news_page.html'}),  #Новости о разработке
    #(r'^null/', direct_to_template, {'template': 'null_page.html'}),    #пустая страница
    
    #(r'^bookmarks/', include('bookmarks.urls')),                        #закладки
    
    #(r'^business_trips/', include('report.business_trips.urls')),       #журнал поездок
    
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_media}),
    #(r'^site_upload/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_upload}),
    #(r'^backup/(?P<path>.*)$', 'django.views.static.serve',{'document_root': backup_dir}),
)
