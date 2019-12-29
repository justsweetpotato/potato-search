#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('obelisk/', views.obelisk, name='obelisk'),
    path('obelisk_beta/', views.obelisk_beta, name='obelisk_beta'),
]
