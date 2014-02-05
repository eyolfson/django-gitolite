# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import pwd
import subprocess

from django.conf import settings

logger = logging.getLogger('gitolite')

def home_dir():
    return pwd.getpwnam(settings.GITOLITE_USER).pw_dir

def key_abspath(key):
    filename = '{}@django-{}.pub'.format(key.user.username, key.pk)
    return os.path.join(home_dir(), '.gitolite', 'keydir', filename)

def ssh_authkeys():
    command = ['gitolite', 'trigger', 'SSH_AUTHKEYS']
    if pwd.getpwuid(os.getuid()).pw_name != settings.GITOLITE_USER:
        command = ['sudo', '-n', '-u', settings.GITOLITE_USER] + command
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' returned {}" 
        logger.error(msg.format(' '.join(e.cmd), e.returncode))

def receive_key_create(sender, instance, **kwargs):
    path = key_abspath(instance)
    try:
        with open(path, 'w') as f:
            f.write(instance.data)
            f.write('\n')
        ssh_authkeys()
    except:
        msg = "key with path '{}' not created"
        logger.error(msg.format(path))

def receive_key_delete(sender, instance, **kwawgs):
    path = key_abspath(instance)
    try:
        os.remove(path)
        ssh_authkeys()
    except:
        msg = "key with path '{}' not deleted"
        logger.error(msg.format(path))
