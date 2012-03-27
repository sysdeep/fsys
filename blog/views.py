# -*- coding: utf-8 -*-
#blog/views

#django----------
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


#local-----------
from blog.models import Note, Tag, SharedNote
from blog.forms import NoteSaveForm, SearchForm




#-----------------------------------------------------------------------
def note_page(request, note_id):
    """Страница 1 записи"""
    
    if request.user:
        print "===================user"
    else:
        print "==================no"
    note = Note.objects.get(id=note_id)
    
    variables = RequestContext(request, {
        'note': note,
        'show_link': False,
    })
    return render_to_response(u'blog/note_page.html', variables)
#-----------------------------------------------------------------------





#-----------------------------------------------------------------------
def main_page(request):
    """Главная страница"""
    
    
    shared_notes = SharedNote.objects.order_by("-date")[:10]
    #users = User.objects.all()
    
    #sites = Link.objects.all()
    
    
    variables = RequestContext(request,{
        #'sites': sites,
        #'users': users,
        #'shared_bookmarks': shared_bookmarks,
        'foo': "foo",
        'shared_notes': shared_notes,
    })
    
    return render_to_response(u"blog/main_page.html", variables)
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
@login_required
def note_save_page(request):
    """Сохранение записи"""
   
    if request.method == 'POST':    #отправка данных
        form = NoteSaveForm(request.POST)
        if form.is_valid():
			
			if 'id' in request.POST:				#если есть id в запросе - меняем запись
				note_id = request.POST["id"]
				note = Note.objects.get(id=note_id)
				
				note.tag_set.clear()				#чистим список старых тегов
				
			else:										#новая запись
				note = Note()
				note.user = request.user
				
				
			note.title = form.cleaned_data["title"]
			note.desc = form.cleaned_data["desc"]
			note.save()             #сохраняем



			tag_names = form.cleaned_data["tags"].split()   			#список тегов
			
			for tag_name in tag_names:
				tag, dummy = Tag.objects.get_or_create(
					name = tag_name
				)
						
				note.tag_set.add(tag)
            
                
            #Расшаривание
			if form.cleaned_data['share']:
				shared, created = SharedNote.objects.get_or_create(note=note)
				if created:
					shared.users_voted.add(request.user)
					shared.save()
            
            
            
            # прыгаем на запись
			return HttpResponseRedirect('/blog/user/%s/' % request.user.username)
            
    elif 'id' in request.GET:
        id = request.GET["id"]
        title = ''
        desc = ''
        try:
            
            note = Note.objects.get(id=id, user=request.user)
            title = note.title
            desc = note.desc
            tags = ' '.join(tag.name for tag in note.tag_set.all())
        except (Note.DoesNotExist):
            pass
        form = NoteSaveForm({
            'title': title,
            'desc': desc,
            'tags': tags,
        })
        note_id = id
    else:
        
        form = NoteSaveForm()
        note_id=""
    
    variables = RequestContext(request,{
        'form': form,
        'note_id': note_id,
    })
    
    
    return render_to_response(u'blog/blog_save_page.html', variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
def user_page(request, username):
    """Страница выбранного пользователя"""
    
    
    #try:        #пробуем
    #    user = User.objects.get(username=username)      #если есть - получаем
    #except User.DoesNotExist:                           #нет такого пользователя - ошибка
    #    raise Http404(u"User "+username+" not found")
     
    user = get_object_or_404(User, username=username) 
        
    notes = user.note_set.order_by("-id")     #все записи
    
    #show_link = True
    
    variables = RequestContext(request,{
        'username': user,
        'notes': notes,
        'show_link': True,
    })
    
    return render_to_response(u"blog/user_page.html", variables)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
@login_required
def note_safe_delete_page(request):
    """Страничка с предупреждением об удалении записи"""
    
    id = request.GET["id"]
    note = Note.objects.get(id=id, user=request.user)
    variables = RequestContext(request, {
        'note': note,
    })
    
    return render_to_response('blog/safe_delete.html', variables)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
@login_required
def note_delete_page(request):
    """Удалении записи"""
    
    id = request.GET["id"]
    note = Note.objects.get(id=id, user=request.user)
    note.delete()
    return HttpResponseRedirect('/blog/user/%s/' % request.user.username)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
def tag_page(request, tag_name):
    """Страница записей с заданным тэгом"""
    
    tag = get_object_or_404(Tag, name=tag_name)
    notes = tag.notes.order_by('-id')
    variables = RequestContext(request,{
        'notes': notes,
        'tag_name': tag_name,
        'show_link': True,
    })
    return render_to_response(u'blog/tag_page.html', variables)
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def tag_cloud_page(request):
    """Облако тэгов"""
    
    MAX_W = 5
    tags = Tag.objects.order_by("name")
    #min и max кол-во тэгов
    min_count = max_count = tags[0].notes.count()
    for tag in tags:
        tag.count = tag.notes.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
    #диапазон
    range = float(max_count-min_count)
    if range == 0.0:
        range = 1.0
        
    for tag in tags:
        tag.weight = int(MAX_W*(tag.count-min_count)/range)
        
    variables = RequestContext(request,{
        'tags': tags,
    })
    
    return render_to_response(u'blog/tag_cloud_page.html', variables)
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def search_page(request):
    """Поиск"""
    
    form = SearchForm()
    notes=[]
    if 'query' in request.GET:
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            notes = Note.objects.filter(title__icontains=query)[:10]
            
    variables = RequestContext(request, {
        "form": form,
        "notes": notes,
        'show_link': True,
    })
    
    return render_to_response(u'blog/search.html', variables)
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











