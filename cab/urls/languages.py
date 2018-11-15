from django.urls import path

from ..views import languages

urlpatterns = [
    path('', languages.language_list, name='cab_language_list'),
    path('<slug:slug>/', languages.language_detail, name='cab_language_detail'),
]
