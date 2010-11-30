# -*- coding: utf-8 -*-
#bookmarks/forms

#django----------
from django import forms
#import re
#from django.contrib.auth.models import User


#-----------------------------------------------------------------------
class BookmarkSaveForm(forms.Form):
    """Форма закладки"""
    
    url = forms.URLField(label=u"URL", widget=forms.TextInput(attrs={'size':64}))
    
    title = forms.CharField(label=u"Title", widget=forms.TextInput(attrs={'size':64}))
    
    tags = forms.CharField(label=u"Tags", widget=forms.TextInput(attrs={'size':64}), required=False)
    
    share = forms.BooleanField(label=u'Share on the main page', required=False)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
class SearchForm(forms.Form):
    """Поиск"""
    
    query = forms.CharField(label=u'Введите ключевое слово', widget=forms.TextInput(attrs={'size': 32, 'class': "form_input",}))
#-----------------------------------------------------------------------
