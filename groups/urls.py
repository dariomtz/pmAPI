from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.groups_view, name='groups'),
    path('<int:groupId>/', views.single_group_view, name='groups'),
    path('<int:groupId>/projects/', views.add_project_group, name='groups'),
]
