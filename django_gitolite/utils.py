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

def gitolite_command_prefix():
    command = ['gitolite']
    if pwd.getpwuid(os.getuid()).pw_name != settings.GITOLITE_USER:
        command = ['sudo', '-n', '-u', settings.GITOLITE_USER] + command
    return command

def ssh_authkeys():
    command = gitolite_command_prefix() + ['trigger', 'SSH_AUTHKEYS']
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' returned {}" 
        logger.error(msg.format(' '.join(e.cmd), e.returncode))
    except Exception as e:
        msg = "command '{}' exception '{}'"
        logger.error(msg.format(' '.join(command), e))

def receive_key_create(sender, instance, **kwargs):
    path = key_abspath(instance)
    try:
        with open(path, 'w') as f:
            f.write(instance.body)
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
