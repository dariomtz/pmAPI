from django.urls import path, include
from . import views

urlpatterns = [
    path('projects/', include('projects.urls')),
]