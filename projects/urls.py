from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_projects, name='all-projects'),
    path('<uuid:projectId>/', views.specific_project, name='specific-project'),
    path('<uuid:projectId>/<uuid:taskId>/', views.specific_task, name='specific-task')
]