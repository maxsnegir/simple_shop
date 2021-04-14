from django.contrib.auth.forms import UserCreationForm

from .models import Customer


class RegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']
