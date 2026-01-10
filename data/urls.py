from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.date_list, name='date_list'),
    path('<str:date>/', views.date_detail, name='date_detail'),
]

