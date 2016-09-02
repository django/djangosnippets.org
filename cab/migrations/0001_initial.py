# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('language_code', models.CharField(max_length=50)),
                ('mime_type', models.CharField(max_length=100)),
                ('file_extension', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('description_html', models.TextField(editable=False)),
                ('code', models.TextField()),
                ('highlighted_code', models.TextField(editable=False)),
                ('version', models.FloatField(
                    default=0,
                    choices=[
                        (1.9, b'1.9'), (1.8, b'1.8'), (1.7, b'1.7'),
                        (1.6, b'1.6'), (1.5, b'1.5'), (1.4, b'1.4'),
                        (1.3, b'1.3'), (1.2, b'1.2'), (1.1, b'1.1'),
                        (1, b'1.0'), (0.96, b'.96'), (0.95, b'Pre .96'),
                        (0, b'Not specified')
                    ],
                )),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('bookmark_count', models.IntegerField(default=0)),
                ('rating_score', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='cab.Language')),
                ('tags', taggit.managers.TaggableManager(
                    to='taggit.Tag',
                    through='taggit.TaggedItem',
                    help_text='A comma-separated list of tags.',
                    verbose_name='Tags',
                )),
            ],
            options={
                'ordering': ('-pub_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnippetFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag', models.IntegerField(choices=[(1, b'Spam'), (2, b'Inappropriate')])),
                ('snippet', models.ForeignKey(related_name='flags', to='cab.Snippet')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='snippet',
            field=models.ForeignKey(related_name='bookmarks', to='cab.Snippet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(related_name='cab_bookmarks', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
