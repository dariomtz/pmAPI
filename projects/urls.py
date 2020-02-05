from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.projects_view, name='projects'),
    path('<int:projectId>/', views.project_view, name='project'),
    path('<int:projectId>/tasks/', views.tasks_view, name='tasks' ),
    path('<int:projectId>/tasks/<int:taskId>/', views.task_view, name='task')
]
