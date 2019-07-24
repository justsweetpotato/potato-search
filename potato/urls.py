#!/usr/bin/env python
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('search', views.search, name='search')
]
