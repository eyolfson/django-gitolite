# Copyright 2014 Jon Eyolfson
#
# This file is part of Django Gitolite.
#
# Django Gitolite is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Django Gitolite is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Django Gitolite. If not, see <http://www.gnu.org/licenses/>.

import importlib
import os
import sys

from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from django_gitolite.models import Push, Repo

class Command(BaseCommand):
    help = 'Handles the git post-update hook for gitolite.'

    def handle(self, **options):
        if 'GL_BYPASS_ACCESS_CHECKS' in os.environ:
            return

        if not 'GL_REPO' in os.environ:
            raise CommandError('Environment variable GL_REPO not set.')
        path = os.environ['GL_REPO']
        repo = Repo.objects.get_or_create(path)[0]

        if not 'GL_USER' in os.environ:
            raise CommandError('Environment variable GL_USER not set.')
        username = os.environ['GL_USER']
        user = get_user_model().objects.get_or_create(username=username)[0]

        pushes = []
        for line in sys.stdin:
            old_rev, new_rev, refname = line.split()
            pushes.append(Push.objects.create(repo=repo, user=user,
                                              old_rev=old_rev, new_rev=new_rev,
                                              refname=refname))

        try:
            hooks = settings.GITOLITE_HOOKS
        except AttributeError:
            hooks = []
        for h in hooks:
            module_name, function_name = h.rsplit('.', maxsplit=1)
            m = importlib.import_module(module_name)
            f = getattr(m, function_name)
            for push in pushes:
                f(push)
