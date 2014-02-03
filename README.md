# Django Gitolite App

Provides a basic front-end for Gitolite.

## Gitolite Configuration

1. Add `LOCAL_CODE => "$rc{GL_ADMIN_BASE}/local",` to the rc file.
2. Add `POST_COMPILE => ['django'],` to the rc file.
3. Add `POST_CREATE => ['django'],` to the rc file.
4. Add `SSH_AUTHKEYS => ['post-compile/ssh-authkeys'],` to the rc file.
5. Add `local/triggers/django`, it should call the `gitolitetrigger` command.
6. Add `local/hooks/common/post_receive`, it should call the `gitolitehook`
   command.

Below is an example script to call the `gitolitetrigger` command.

    #!/bin/bash
    python /srv/git/site/manage.py gitolitetrigger $@

## License

Except where noted, all code is licensed under GPL v3.
