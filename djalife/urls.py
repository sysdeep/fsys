# -*- coding: utf-8 -*-
#--- djlife.urls ---

#--- python
import os.path

#--- django
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#--- local
from settings import site_media
from views import logout_page, register_page

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
    
    
    
    (r'^$', direct_to_template, {'template': 'main_page.html'}),        #main
    (r'^about/', direct_to_template, {'template': 'about/about_page.html'}),  #about
    (r'^about_news/', direct_to_template, {'template': 'about/about_news_page.html'}),  #Новости о разработке
    (r'^null/', direct_to_template, {'template': 'null_page.html'}),    #пустая страница
    
    (r'^bookmarks/', include('bookmarks.urls')),                        #закладки
    (r'^blog/', include('blog.urls')),                        #закладки
    
    
    (r'^login/$', 'django.contrib.auth.views.login'),                   #login
    (r'^logout/', logout_page),                                         #logout
    (r'^register/', register_page),                                     #регистрация
    (r'^register_success/', direct_to_template, {'template': 'registration/register_success.html'}),    #
    
    
     (r'^login_help/', direct_to_template, {'template': 'login_help.html'}),  #помощь при регистрации
    
    
    
    
    (r'^comments/', include('django.contrib.comments.urls')),           #комментарии

    
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_media}),
    #(r'^site_upload/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_upload}),
    #(r'^backup/(?P<path>.*)$', 'django.views.static.serve',{'document_root': backup_dir}),
)
