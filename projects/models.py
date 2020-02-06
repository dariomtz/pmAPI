from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User, blank=True, related_name='projects', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, related_name='projects', on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    deadline = models.DateTimeField()
    #inCharge = models.ManyToManyField(Group, related_name='tasks')
    resources = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

