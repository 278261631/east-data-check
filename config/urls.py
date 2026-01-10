from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return redirect('data:date_list')


urlpatterns = [
    path("east-admin/", admin.site.urls),
    path("east-accounts/", include("accounts.urls")),
    path("east-data/", include("data.urls")),
    path("", home, name="home"),
]
