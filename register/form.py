from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Customer


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, label='Имя',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='Фамилия',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label='Email',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}), )
