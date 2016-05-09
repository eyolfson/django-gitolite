# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

import os
import re

from collections import namedtuple
from subprocess import check_output, STDOUT, CalledProcessError

class Version(namedtuple('Version', ['major', 'minor', 'patch', 'extra'])):

    def __str__(self):
        s = '{}.{}.{}'.format(self.major, self.minor, self.patch)
        if self.extra:
            return '{}-{}'.format(s, self.extra)
        return s

def get_version():
    version = Version(0, 1, 7, '')

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    GIT_DIR = os.path.join(BASE_DIR, '.git')
    if not os.path.isdir(GIT_DIR):
        return version

    try:
        output = check_output(['git', '--git-dir={}'.format(GIT_DIR),
                               '--work-tree={}'.format(BASE_DIR),
                               'describe', '--abbrev=6', '--match', 'v*',
                               '--dirty=-dirty'], stderr=STDOUT)
    except CalledProcessError:
        return version

    output = output.strip().decode()
    match = re.match('v([0-9]+)\.([0-9]+)\.([0-9]+)-(.*)', output)
    if not match:
        return version
    return Version(int(match.group(1)), int(match.group(2)),
                   int(match.group(3)), match.group(4))
