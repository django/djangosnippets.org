from django.urls import path

from ..views import popular

urlpatterns = [
    path('languages/', popular.top_languages, name='cab_top_languages'),
    path('bookmarked/', popular.top_bookmarked, name='cab_top_bookmarked'),
    path('rated/', popular.top_rated, name='cab_top_rated'),
]
