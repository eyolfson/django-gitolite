# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_delete

from eyl.django.ssh.models import Key

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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                related_name='created_repos')
    forked_from = models.ForeignKey('self', blank=True, null=True,
                                    related_name='forked_repos')
    objects = RepoManager()

    def __str__(self):
        return self.path

    def sync(self):
        git_path = os.path.join(os.environ['HOME'], 'repositories',
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

    class Meta:
        ordering = ['path']

class Push(models.Model):
    repo = models.ForeignKey(Repo, related_name='pushes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pushes')
    time = models.DateTimeField(auto_now_add=True)
    old_rev = models.CharField(max_length=40)
    new_rev = models.CharField(max_length=40)
    refname = models.TextField(db_index=True)

class Access(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accesses')
    repo = models.ForeignKey(Repo, related_name='accesses')

    class Meta:
        unique_together = ('user', 'repo')
        ordering = ['repo', 'user']

def get_filename(key):
    filename = '{}@django-{}.pub'.format(key.user.username, key.pk)
    return filename

def get_gitolite_path(key):
    keydir = os.path.join(os.environ['HOME'], '.gitolite', 'keydir')
    return os.path.join(keydir, get_filename(key))

def ssh_authkeys():
    from subprocess import call, DEVNULL
    call(['gitolite', 'trigger', 'SSH_AUTHKEYS'], stdout=DEVNULL,
         stderr=DEVNULL)

def add_key(sender, instance, **kwargs):
    abspath = get_gitolite_path(instance)
    try:
        with open(abspath, 'w') as f:
            f.write(instance.data)
            f.write('\n')
    except:
        pass
    ssh_authkeys()

def remove_key(sender, instance, **kwargs):
    abspath = get_gitolite_path(instance)
    try:
        os.remove(abspath)
    except:
        pass
    ssh_authkeys()

post_save.connect(add_key, Key)
pre_delete.connect(remove_key, Key)
