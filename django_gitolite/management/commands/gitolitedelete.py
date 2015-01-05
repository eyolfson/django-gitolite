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

import os

from subprocess import check_call, DEVNULL

from django.core.management.base import BaseCommand, CommandError

from django_gitolite.models import Repo
from django_gitolite.utils import gitolite_command_prefix

class Command(BaseCommand):
    args = '<repo_path repo_path ...>'
    help = 'Handles deleting git repositories through gitolite.'

    def handle(self, *args, **options):
        for repo_path in args:
            try:
                repo = Repo.objects.get(path=repo_path)
                user = repo.creator
                if user == None:
                    msg = 'Repo "{}" is not a wildcard.'
                    raise CommandError(msg.format(repo_path))
                username = user.username
                os.environ['GL_USER'] = username
                check_call(gitolite_command_prefix()
                           + ['D', 'unlock', repo_path],
                           stdout=DEVNULL, stderr=DEVNULL)
                check_call(gitolite_command_prefix()
                           + ['D', 'rm', repo_path],
                           stdout=DEVNULL, stderr=DEVNULL)
                repo.delete()
            except Repo.DoesNotExist:
                msg = 'Repo {} does not exist.'
                raise CommandError(msg.format(repo_path))
