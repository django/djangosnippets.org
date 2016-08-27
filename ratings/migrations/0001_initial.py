# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0, db_index=True)),
                ('hashed', models.CharField(max_length=40, editable=False, db_index=True)),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(related_name='rated_items', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='rateditems', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimilarItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('similar_object_id', models.IntegerField()),
                ('score', models.FloatField(default=0)),
                ('content_type', models.ForeignKey(related_name='similar_items', to='contenttypes.ContentType')),
                ('similar_content_type', models.ForeignKey(related_name='similar_items_set', to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
