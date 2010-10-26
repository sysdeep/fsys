# -*- coding: utf-8 -*-
#bookmarks/views

#django----------
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

from django.shortcuts import render_to_response  #, get_object_or_404


#local-----------
from bookmarks.models import Link


#-----------------------------------------------------------------------
def main_page(request):
    """Главная страница"""
    
    users = User.objects.all()
    
    sites = Link.objects.all()
    
    
    variables = ({
        'sites': sites,
        'users': users,
    })
    
    return render_to_response(u"bookmarks/main_page.html", variables)
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
def user_page(request, username):
    """Страница выбранного пользователя"""
    
    
    try:        #пробуем
        user = User.objects.get(username=username)      #если есть - получаем
    except User.DoesNotExist:                           #нет такого пользователя - ошибка
        raise Http404(u"User "+username+" not found")
        
    bookmarks = user.bookmark_set.all()     #все закладки
    
    variables = ({
        'username': user,
        'bookmarks': bookmarks,
    })
    
    return render_to_response(u"bookmarks/user_page.html", variables)
#-----------------------------------------------------------------------
