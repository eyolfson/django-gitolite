# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

from django.urls import path

from django_gitolite import views

app_name = 'git'
urlpatterns = [
    path('', views.index, name='index'),
    path('<path:path>/', views.repo, name='repo'),
]
