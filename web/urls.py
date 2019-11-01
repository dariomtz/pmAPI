from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='wellcome' ),
    path('login/', views.login, name='login' ),
    path('projects/', views.app, name='app' ),
]