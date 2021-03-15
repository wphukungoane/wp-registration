from django.contrib import admin
from . import models
from .models import ProjectInfo


class ProjectsInLine(admin.TabularInline):
    model = models.ProjectInfo
    extra = 0

def Make_Approved(modeladmin, request, queryset):
    queryset.update(status='Approved')
Make_Approved.short_description = "Mark selected projects as Approved"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_code','Project_Name', 'Project_Owner','status']
    ordering = ['project_code']
    search_fields = ('Project_Name', 'Project_Owner')
    actions = [Make_Approved]

class ResourceAdmin(admin.ModelAdmin):
    list_display = ['Number_CPU', 'Memory_required', 'Storage','OS_Type']
    ordering = ['OS_Type']



admin.site.register(ProjectInfo, ProjectAdmin)
