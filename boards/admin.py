from django.contrib import admin

from .models import Board, Project, Post

admin.site.register(Board)
admin.site.register(Project)
admin.site.register(Post)
