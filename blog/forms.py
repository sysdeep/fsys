# -*- coding: utf-8 -*-
#blog/forms

#django----------
from django import forms
#import re
#from django.contrib.auth.models import User


#-----------------------------------------------------------------------
class NoteSaveForm(forms.Form):
    """Форма"""
        
    title = forms.CharField(label=u"Название", widget=forms.TextInput(attrs={'size':64}), required=True)
    
    desc = forms.CharField(label=u"Текст", widget=forms.Textarea(attrs={'size':64}), required=True)
    
    tags = forms.CharField(label=u"Тэги", widget=forms.TextInput(attrs={'size':64}), required=False)
    
    share = forms.BooleanField(label=u'Показывать на главной', required=False)
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
class SearchForm(forms.Form):
    """Поиск"""
    
    query = forms.CharField(label=u'Введите ключевое слово', widget=forms.TextInput(attrs={'size': 32, 'class': "form_input",}))
#-----------------------------------------------------------------------
