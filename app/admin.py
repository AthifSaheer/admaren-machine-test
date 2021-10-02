from django.contrib import admin
from .models import Tag, Snippet

admin.site.register([Tag, Snippet])