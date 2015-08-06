# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

from django.conf.urls import url

from django_gitolite import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<path>([A-Za-z0-9-+_]+/)*[A-Za-z0-9-+_]+)/$',
        views.repo, name='repo'),
]
