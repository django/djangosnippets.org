from django.urls import path

from ..views import popular

urlpatterns = [
    path("languages/", popular.top_languages, name="cab_top_languages"),
]
