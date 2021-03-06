from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from register.forms import RegisterForm


class Logout(LogoutView):
    template_name = 'registration/logged_out.html'


class Login(LoginView):
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('index')


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('register:login')
    template_name = 'registration/register.html'
