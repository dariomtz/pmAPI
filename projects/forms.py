from django.forms import ModelForm
from .models import Project, Task

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'tasks',
            'deadline',
            'status',
        ]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'deadline',
            'startDate',
            'resources',
            'status',
        ]


