"""Admin for the Network app."""

# pylint: skip-file
from django.contrib import admin
from .models import User, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
