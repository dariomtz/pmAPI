from django.db import models
from django.contrib.auth.models import User, Group

class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    #can_read = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='can_read', null=True)
    #can_edit = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='can_edit', null=True)
    #admins = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='admin', null=True)
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

