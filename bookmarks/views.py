# -*- coding: utf-8 -*-
#bookmarks/views

#django----------
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


#local-----------
from bookmarks.models import Link, Bookmark, Tag, SharedBookmark
from bookmarks.forms import BookmarkSaveForm, SearchForm




#-----------------------------------------------------------------------
def bookmark_page(request, bookmark_id):
    """Страница 1 записи"""
    shared_bookmark = get_object_or_404(SharedBookmark, id=bookmark_id)
    
    variables = RequestContext(request, {
        'shared_bookmark': shared_bookmark,
    })
    return render_to_response(u'bookmarks/bookmark_page.html', variables)
#-----------------------------------------------------------------------





#-----------------------------------------------------------------------
def main_page(request):
    """Главная страница"""
    
    
    shared_bookmarks = SharedBookmark.objects.order_by("-date")[:10]
    #users = User.objects.all()
    
    #sites = Link.objects.all()
    
    
    variables = RequestContext(request,{
        #'sites': sites,
        #'users': users,
        'shared_bookmarks': shared_bookmarks,
    })
    
    return render_to_response(u"bookmarks/main_page.html", variables)
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
def user_page(request, username):
    """Страница выбранного пользователя"""
    
    
    #try:        #пробуем
    #    user = User.objects.get(username=username)      #если есть - получаем
    #except User.DoesNotExist:                           #нет такого пользователя - ошибка
    #    raise Http404(u"User "+username+" not found")
     
    user = get_object_or_404(User, username=username) 
        
    bookmarks = user.bookmark_set.order_by("-id")     #все закладки
    
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
                
            #Расшаривание
            if form.cleaned_data['share']:
                shared, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
                if created:
                    shared.users_voted.add(request.user)
                    shared.save()
            
            
            bookmark.save()             #сохраняем
            
            return HttpResponseRedirect('/bookmarks/user/%s/' % request.user.username)
            
    elif 'url' in request.GET:
        url = request.GET["url"]
        title = ''
        tags = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(link=link, user=request.user)
            title = bookmark.title
            tags = ' '.join(tag.name for tag in bookmark.tag_set.all())
        except (Link.DoesNotExist, Bookmark.DoesNotExist):
            pass
        form = BookmarkSaveForm({
            'url': url,
            'title': title,
            'tags': tags,
        })
    else:
        
        form = BookmarkSaveForm()
    
    variables = RequestContext(request,{
        'form': form,
    })
    
    
    return render_to_response(u'bookmarks/bookmark_save_page.html', variables)
#-----------------------------------------------------------------------





#-----------------------------------------------------------------------
def tag_page(request, tag_name):
    """Страница закладок с заданным тэгом"""
    
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = RequestContext(request,{
        'bookmarks': bookmarks,
        'tag_name': tag_name,
    })
    return render_to_response(u'bookmarks/tag_page.html', variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def tag_cloud_page(request):
    """Облако тэгов"""
    
    MAX_W = 5
    tags = Tag.objects.order_by("name")
    #min и max кол-во тэгов
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag_count
    #диапазон
    range = float(max_count-min_count)
    if range == 0.0:
        range = 1.0
        
    for tag in tags:
        tag.weight = int(MAX_W*(tag.count-min_count)/range)
        
    variables = RequestContext(request,{
        'tags': tags,
    })
    
    return render_to_response(u'bookmarks/tag_cloud_page.html', variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def search_page(request):
    """Поиск"""
    
    form = SearchForm()
    bookmarks=[]
    if 'query' in request.GET:
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
            
    variables = RequestContext(request, {
        "form": form,
        "bookmarks": bookmarks,
    })
    #if request.GET.has_key('ajax'):
        #print "ajax!!!!!!!!!!!!"
        #return render_to_response(u'bookmarks/search.html', variables)
    #else:
        #print "No Ajax"
    return render_to_response(u'bookmarks/search.html', variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
@login_required
def bookmark_vote_page(request):
    """Рейтинги"""
    if 'id' in request.GET:
        try:
            id = request.GET['id']
            shared_bookmark = SharedBookmark.objects.get(id=id)
            user_voted = shared_bookmark.users_voted.filter(username=request.user.username)
            if not user_voted:
                shared_bookmark.votes += 1
                shared_bookmark.users_voted.add(request.user)
                shared_bookmark.save()
        except SharedBookmark.DoesNotExist:
            raise Http404('Bookmark not found.')
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
from datetime import datetime, timedelta
def popular_page(request):
    """Популярные"""
    today = datetime.today()
    yesterday = today - timedelta(1)
    shared_bookmarks = SharedBookmark.objects.filter(date__gt=yesterday)
    shared_bookmarks = shared_bookmarks.order_by('-votes')[:10]
    variables = RequestContext(request, {
        'shared_bookmarks': shared_bookmarks
    })
    return render_to_response('bookmarks/popular_page.html', variables)
#-----------------------------------------------------------------------











