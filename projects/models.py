from django.db import models
from django.contrib.auth.models import User, Group

class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(blank=True)
    can_read = models.ForeignKey(Group, on_delete=models.SET_NULL)
    can_edit = models.ForeignKey(Group, on_delete=models.SET_NULL)
    admins = models.ForeignKey(Group, on_delete=models.SET_NULL)
    tasks = models.ManyToManyField('Task')
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False)

class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    startDate = models.DateTimeField()
    inCharge = models.ManyToManyField(Group, on_delete=models.SET_NULL)
    resources = models.CharField(blank=True)

