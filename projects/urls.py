from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_projects, name='all-projects'),
    path('<int:projectId>/', views.specific_project, name='specific-project'),
    path('<int:projectId>/<int:taskId>/', views.specific_task, name='specific-task')
]