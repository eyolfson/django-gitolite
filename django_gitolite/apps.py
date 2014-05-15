# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class GitoliteConfig(AppConfig):
    name = 'django_gitolite'

    def ready(self):
        if not hasattr(settings, 'GITOLITE_USER'):
            raise ImproperlyConfigured("'GITOLITE_USER' not set")
