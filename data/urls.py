from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.date_list, name='date_list'),
    path('<str:date>/', views.date_detail, name='date_detail'),
    path('<str:date>/row/<int:row_index>/files/', views.row_files, name='row_files'),
    path('<str:date>/image/<str:filename>', views.serve_image, name='serve_image'),
    path('<str:date>/fits/<str:filename>', views.serve_fits, name='serve_fits'),
    path('<str:date>/status/', views.get_status, name='get_status'),
    path('<str:date>/status/update/', views.update_status, name='update_status'),
    path('<str:date>/row/<int:row_index>/judge/', views.submit_judgment, name='submit_judgment'),
    path('<str:date>/row/<int:row_index>/remark/', views.submit_remark, name='submit_remark'),
    path('<str:date>/judgments/', views.get_judgments, name='get_judgments'),
    path('<str:date>/sync-rows/', views.sync_excel_rows, name='sync_excel_rows'),
]

