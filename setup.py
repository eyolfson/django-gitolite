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

from distutils.core import setup

setup(
    name = 'django-gitolite',
    packages = ['django_gitolite',
                'django_gitolite.management',
                'django_gitolite.management.commands'],
    version = '0.1.7',
    description = 'A basic Django app for using Gitolite',
    author = 'Jon Eyolfson',
    author_email = 'jon@eyl.io',
    url = 'https://github.com/eyolfson/django-gitolite/',
    download_url = ('https://github.com/eyolfson/django-gitolite/archive/'
                    'v0.1.7.tar.gz'),
)
