# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 21:25:16 2017

@author: nath
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]