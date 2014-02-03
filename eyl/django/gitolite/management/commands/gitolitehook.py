# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand, CommandError

from eyl.django.gitolite.models import Push, Repo

class Command(NoArgsCommand):
    help = 'Handles the git post-update hook for gitolite.'

    def handle_noargs(self, **options):
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

        old_rev, new_rev, refname = sys.stdin.read().split()
        push = Push.objects.create(repo=repo, user=user, old_rev=old_rev,
                                   new_rev=new_rev, refname=refname)
