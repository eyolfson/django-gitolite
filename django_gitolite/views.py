# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django_gitolite.models import Access, Push, Repo

@login_required
def index(request):
    return render(request, 'gitolite/index.html',
                  {'accesses': Access.objects.filter(user=request.user)})
