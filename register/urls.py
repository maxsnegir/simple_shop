from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
]
