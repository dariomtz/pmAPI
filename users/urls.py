from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_users, name='all-users'),
]