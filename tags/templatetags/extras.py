# -*- coding: utf-8 -*-
#/tags/templatetags/extras.py
#необходимо зарегистрировать в settings.py - INSTALLED_APPS

from django import template

from djalife.settings import VERSION

register = template.Library()


def pro_version(value):
    '''Возвращает версию проекта'''
    
    return VERSION


#регестрирование tag
register.filter('pro_version', pro_version)
