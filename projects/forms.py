from django.forms import ModelForm
from .models import Project, Task

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'deadline',
            'status',
            'public'
        ]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'deadline',
            'resources',
            'status',
        ]


