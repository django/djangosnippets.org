from django.conf.urls import url, patterns, include

from cab.views import accounts

urlpatterns = patterns('',
    url(r'^',
        include('django.contrib.auth.urls')),
    url(r'^register/$',
        accounts.CabRegistrationView.as_view(),
        name='registration_register'),
    url(r'^',
        include('registration.backends.default.urls')),
)
