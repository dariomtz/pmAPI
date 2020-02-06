from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.groups_view, name='projects'),
]
