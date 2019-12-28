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

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse

from django_ssh.models import Key
from django_gitolite.utils import (
    home_dir,
    receive_key_create,
    receive_key_delete
)

class RepoManager(models.Manager):

    def get_or_create(self, path):
        created = False
        try:
            repo = Repo.objects.get(path=path)
        except Repo.DoesNotExist:
            repo = Repo(path=path)
            repo.sync()
            repo.save()
            created = True
        return (repo, created)

class Repo(models.Model):
    path = models.TextField(db_index=True, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE,
                                related_name='created_repos')
    forked_from = models.ForeignKey('self',
                                    blank=True,
                                    null=True,
                                    on_delete=models.CASCADE,
                                    related_name='forked_repos')
    objects = RepoManager()

    def __str__(self):
        return self.path

    def sync(self):
        git_path = os.path.join(home_dir(), 'repositories',
                                '{}.git'.format(self.path))
        self.creator = None
        try:
            with open(os.path.join(git_path, 'gl-creator')) as f:
                d = f.read().strip()
                self.creator = get_user_model().objects.get_or_create(
                    username=d)[0]
        except IOError:
            pass
        self.forked_from = None
        try:
            with open(os.path.join(git_path, 'gl-forked-from')) as f:
                d = f.read().strip()
                self.forked_from = Repo.objects.get_or_create(d)[0]
        except IOError:
            pass

    def get_absolute_url(self):
        return reverse('git:repo', args=[self.path])

    class Meta:
        db_table = 'gitolite_repo'
        ordering = ['path']

class Push(models.Model):
    repo = models.ForeignKey(Repo,
                             on_delete=models.CASCADE,
                             related_name='pushes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='pushes')
    time = models.DateTimeField(auto_now_add=True)
    old_rev = models.CharField(max_length=40)
    new_rev = models.CharField(max_length=40)
    refname = models.TextField(db_index=True)

    def __str__(self):
        return '{} {} {} {}'.format(self.repo, self.old_rev,
                                    self.new_rev, self.refname)

    class Meta:
        db_table = 'gitolite_push'

class Access(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='accesses')
    repo = models.ForeignKey(Repo,
                             on_delete=models.CASCADE,
                             related_name='accesses')

    class Meta:
        db_table = 'gitolite_access'
        ordering = ['repo', 'user']
        unique_together = ('user', 'repo')

# Signals
post_save.connect(receive_key_create, Key)
pre_delete.connect(receive_key_delete, Key)
