from django.db import models
from django.contrib.auth.models import User, Group

class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    individual = models.BooleanField(default=True)
    author = models.OneToOneField(User, blank=True, related_name='projects', on_delete=models.CASCADE)
    tasks = models.ManyToManyField('Task',blank=True, related_name='projects')
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    #inCharge = models.ManyToManyField(Group, related_name='tasks')
    resources = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

