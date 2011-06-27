import datetime

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list

from taggit.models import Tag

from cab.models import Snippet, Language, Bookmark
from cab.utils import month_object_list


def top_authors(request):
    return object_list(
        request,
        queryset=Snippet.objects.top_authors(),
        template_name='cab/top_authors.html',
        paginate_by=20)

def top_languages(request):
    return object_list(
        request,
        queryset=Language.objects.top_languages(),
        template_name='cab/language_list.html',
        paginate_by=20)

def top_tags(request):
    return object_list(
        request,
        queryset=Snippet.objects.top_tags(),
        template_name='cab/tag_list.html',
        paginate_by=20,
    )

def top_bookmarked(request):
    queryset = Snippet.objects.most_bookmarked()
    
    return month_object_list(
        request,
        queryset=queryset,
        template_name='cab/most_bookmarked.html',
        paginate_by=20,
    )

def top_rated(request):
    queryset = Snippet.objects.top_rated()
    
    return month_object_list(
        request,
        queryset=queryset,
        template_name='cab/top_rated.html',
        paginate_by=20,
    )
