# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import io

from subprocess import check_output, Popen, DEVNULL, PIPE

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from eyl.django.gitolite.models import Access, Push, Repo

def get_user_list():
    return list(get_user_model().objects.all())

class Command(BaseCommand):
    args = '<name [path [username operation]]>'
    help = 'Handles gitolite triggers'

    def handle(self, name, *args, **options):
        if name == 'POST_COMPILE':
            if len(args) != 0:
                raise CommandError('Invalid number of arguments for POST_COMPILE.')
            self.post_compile()
        elif name == 'POST_CREATE':
            if not len(args) in (1, 3):
                raise CommandError('Invalid number of arguments for POST_CREATE.')
            if len(args) == 1:
                # This is just a normal create, it'll be handled by POST_COMPILE
                return
            self.post_create(*args)


    def sync(self, path, user_list=get_user_list()):
        repo, created = Repo.objects.get_or_create(path)
        # Ensure the repo is synced with gitolite
        if not created:
            repo.sync()
            repo.save()
        Access.objects.filter(repo=repo).delete()
        with Popen(['gitolite', 'access', repo.path, '%', 'R', 'any'],
                   stdin=PIPE, stdout=PIPE, stderr=DEVNULL,
                   universal_newlines=True) as p:

            buf = io.StringIO()
            for user in user_list:
                buf.write(user.username)
                buf.write('\n')
            out, err = p.communicate(buf.getvalue())
            buf.close()

            access_list = []
            for line in out.splitlines():
                path, username, ret = line.strip().split('\t')
                user = get_user_model().objects.get(username=username)
                if not ret.endswith('DENIED by fallthru'):
                    access_list.append(Access(repo=repo, user=user))
                if len(access_list) > 100:
                    Access.objects.bulk_create(access_list)
                    access_list = []
            if len(access_list) != 0:
                Access.objects.bulk_create(access_list)

    def post_compile(self):
        output = check_output(['gitolite', 'list-phy-repos'], stderr=DEVNULL,
                              universal_newlines=True)
        repo_paths = output.splitlines()
        user_list = get_user_list()
        for path in repo_paths:
            self.sync(path, user_list)

    def post_create(self, path, username, operation):
        self.sync(path)
