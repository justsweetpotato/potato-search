#!/usr/bin/env python
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('doc/', views.doc, name='doc'),
    path('api/book', views.api_book, name='api_book'),
    path('api/ip/', views.api_ip, name='api_ip')
]
