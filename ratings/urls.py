from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rate/(?P<ct>\d+)/(?P<pk>[^\/]+)/(?P<score>\-?[\d\.]+)/$', views.rate_object, name='ratings_rate_object'),
    url(r'^unrate/(?P<ct>\d+)/(?P<pk>[^\/]+)/$', views.rate_object, {'add': False}, name='ratings_unrate_object'),
]
