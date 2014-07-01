# Copyright 2014 Jon Eyolfson
#
# This file is distributed under the GPLv3 license

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from django_gitolite.models import Push, Repo

@login_required
def index(request):
    return render(request, 'gitolite/index.html',
                  {'repos': Repo.objects.filter(accesses__user=request.user)})

@login_required
def repo(request, path):
    repo = get_object_or_404(Repo, path=path, accesses__user=request.user)
    pushes = Push.objects.filter(repo=repo)
    return render(request, 'gitolite/repo.html',
                  {'repo': repo, 'pushes': pushes})
