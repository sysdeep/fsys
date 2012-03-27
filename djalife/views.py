# -*- coding: utf-8 -*-
#--- djalife.views

#--- django
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response  #, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import logout



#--- local
#from bookmarks.models import Link
from forms import RegistrationForm



#-----------------------------------------------------------------------
def register_page(request):
    """Регистрация"""
    
    if request.method == 'POST':    #отправка данных
        form = RegistrationForm(request.POST)   #объект - форма с данными
        if form.is_valid():                     #если данные корректны - создаём запись
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register_success/')   #перенаправление
    
    else:       #пустая форма
        form = RegistrationForm()
        
        
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html',variables)
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
def logout_page(request):
    """Выход"""
    logout(request)
    return HttpResponseRedirect('/')
#-----------------------------------------------------------------------
