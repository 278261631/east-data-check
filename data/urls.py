from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.date_list, name='date_list'),
    path('<str:date>/', views.date_detail, name='date_detail'),
    path('<str:date>/row/<int:row_index>/files/', views.row_files, name='row_files'),
    path('<str:date>/image/<str:filename>', views.serve_image, name='serve_image'),
    path('<str:date>/fits/<str:filename>', views.serve_fits, name='serve_fits'),
]

