from cab.forms import RegisterForm
from registration.backends.default.views import RegistrationView


class CabRegistrationView(RegistrationView):
    form_class = RegisterForm
