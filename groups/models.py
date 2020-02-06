from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    admins = models.ManyToManyField(User, related_name='groups_admin')
    members = models.ManyToManyField(User, related_name='groups' )
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)