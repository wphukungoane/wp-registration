from django.contrib import admin

from .models import Profile
from .models import Project

admin.site.register(Profile)
admin.site.register(Project)

