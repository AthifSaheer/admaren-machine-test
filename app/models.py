from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Snippet(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    snippet = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

"""
TAG
timestamp

SNIPPET
tag
user
title
snippet
timestamp
"""