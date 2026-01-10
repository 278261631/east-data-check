from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', lambda r: redirect('accounts:login'), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

