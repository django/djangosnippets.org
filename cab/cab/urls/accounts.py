from django.conf.urls import url, patterns, include

from ratelimitbackend.views import login
from cab.views import accounts

urlpatterns = patterns('',
    url(r'^register/$',
        accounts.CabRegistrationView.as_view(),
        name='registration_register'),
    url(r'^login/$',
        login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^',
        include('registration.backends.default.urls')),
)
