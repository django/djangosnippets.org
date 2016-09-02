# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('keyword', models.TextField(verbose_name='Keyword')),
                ('is_regex', models.BooleanField(default=False, verbose_name='Is a regular expression')),
                ('fields', models.TextField(max_length=255, verbose_name='Fields to check')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'ordering': ('keyword', 'created'),
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
            },
            bases=(models.Model,),
        ),
    ]
