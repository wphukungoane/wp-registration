import django_tables2 as tables
from .models import ProjectInfo

class ProjectTable(tables.Table):
    class Meta:
        model = ProjectInfo
        template_name = "django_tables2/bootstrap.html"
        fields = ('Project_Owner','Name', 'Research_Area', 'Description' )
