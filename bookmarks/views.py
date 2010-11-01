# -*- coding: utf-8 -*-
#bookmarks/views

#django----------
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response  #, get_object_or_404
from django.contrib.auth.decorators import login_required


#local-----------
from bookmarks.models import Link, Bookmark, Tag
from bookmarks.forms import BookmarkSaveForm


#-----------------------------------------------------------------------
def main_page(request):
    """Главная страница"""
    
    users = User.objects.all()
    
    sites = Link.objects.all()
    
    
    variables = RequestContext(request,{
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
    
    variables = RequestContext(request,{
        'username': user,
        'bookmarks': bookmarks,
    })
    
    return render_to_response(u"bookmarks/user_page.html", variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
@login_required
def bookmark_save_page(request):
    """Сохранение закладки"""
   
    if request.method == 'POST':    #отправка данных
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            link, dummy = Link.objects.get_or_create(   #получаем или создаём
                url = form.cleaned_data['url']
            )
            
            bookmark, created = Bookmark.objects.get_or_create( #получаем или создаём
                user = request.user,
                link = link
            )
            
            bookmark.title = form.cleaned_data['title']         #обновляем название
            
            if not created:         #если обновление - чистим список старых тегов
                bookmark.tag_set.clear()
                
            tag_names = form.cleaned_data["tags"].split()   #список тегов
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(
                    name = tag_name
                )
                bookmark.tag_set.add(tag)
            
            bookmark.save()             #сохраняем
            
            return HttpResponseRedirect('/bookmarks/user/%s/' % request.user.username)
    else:
        
        form = BookmarkSaveForm()
    
    variables = RequestContext(request,{
        'form': form,
    })
    
    
    return render_to_response(u'bookmarks/bookmark_save_page.html', variables)
#-----------------------------------------------------------------------

































