# Generated by Django 3.1.5 on 2021-01-14 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField(db_index=True, unique=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_repos', to=settings.AUTH_USER_MODEL)),
                ('forked_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forked_repos', to='django_gitolite.repo')),
            ],
            options={
                'db_table': 'gitolite_repo',
                'ordering': ['path'],
            },
        ),
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('old_rev', models.CharField(max_length=40)),
                ('new_rev', models.CharField(max_length=40)),
                ('refname', models.TextField(db_index=True)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pushes', to='django_gitolite.repo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pushes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'gitolite_push',
            },
        ),
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accesses', to='django_gitolite.repo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accesses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'gitolite_access',
                'ordering': ['repo', 'user'],
                'unique_together': {('user', 'repo')},
            },
        ),
    ]
