import math, uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown
from django.urls import reverse_lazy
from multiselectfield import MultiSelectField
import datetime
from dirtyfields import DirtyFieldsMixin
from django.core.mail import send_mail



def increment_project_number():
    last_project = ProjectInfo.objects.all().order_by('id').last()
    if not last_project:
        return 'NCHOSP-'  + '0000'
    project_code = last_project.project_code
    project_int = int(project_code[8:12])
    new_project_int = project_int + 1
    new_project_code = 'NCHOSP-' +  str(new_project_int).zfill(4)
    return new_project_code


class ProjectInfo(models.Model):

    disciplines = [
                ('Astronomy', 'Astronomy'),
                ('Bioinformatics',  'Bioinformatics'),
                ('Machine Learning',  'Machine Learning'),
                ('Chemistry and Material Science',  'Chemistry and Material Science'),
                ('Computer Science',  'Computer Science'),
                ('Computational Space Physics', 'Computational Space Physics'),
                ('Computational and Fluid Dynamics', 'Computational and Fluid Dynamics'),
                ('Others', 'Other'),]
    Status = [
                ("Pending", "Pending"),
                ("Approved", "Approved"),
                ("Declined", "Declined"),
                ("Completed", "Completed"),]

    images = [
                ("Windows", "Windows"),
                ("Ubuntu", "Ubuntu"),
                ("Centos", "Centos"),
                ("Red hat", "Red hat"),
                ("Suse", "Suse"),
                ("Debian", "Debian"),]


    Approvers = [[ x.username, x.username] for x in User.objects.filter(is_staff=True)]

    Project_Owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    Project_Name = models.CharField(max_length=255)
    Research_Area = models.CharField(max_length=150, choices=disciplines,default='',  blank=True)
    Project_Description = models.TextField(max_length=4000)
    Created_at = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateField(auto_now=True)
    status = models.CharField(max_length=150, choices=Status,default='Pending',  blank=True)
    project_code = models.CharField(max_length =50, default=increment_project_number, editable=False )
    Number_CPU = models.PositiveIntegerField( verbose_name=u"Number of Cores ",   blank=True, default='0')
    Memory_required = models.PositiveIntegerField( verbose_name=u"Memory (GB)",  blank=True, default='0')
    Storage = models.PositiveIntegerField( verbose_name=u"Storage (GB)",  blank=True, default='0')
    Approved_by = models.CharField(max_length =150, choices=Approvers, default='Not Assigned yet',  blank=True )
    OS_Type = models.CharField(max_length=150, choices=images,default='', verbose_name=u"Image",  blank=True)
    Review = models.TextField(verbose_name=u"Recommendation", default='This Project is not yet Reviewed...!',max_length=200)

    class Meta:
        db_table = 'project'
        verbose_name = 'Project List'
        ordering = ['-project_code']

    def __str__(self):
        return self.Project_Name

    def get_initial(self):
        return {'Project_Owner':self.request.user}

    def get_absolute_url(self):
        return reverse_lazy('project-update', kwargs={'pk': self.pk})

    def get_Description_as_markdown(self):
        return mark_safe(markdown(self.Project_Description, safe_mode='escape'))

    def perform_update(self):

        if self.status == 'Approved' and 'status' in self.get_dirty_fields():
            email = {
                'to': 'wphukungoane@gmail.com',
                'cc': 'wphukungoane@gmail.com',
                'subject': 'Project User Registration Recieved from {} {}',
                'message': '{} {} has completed their registration and is ready to be activated by IT',
            }
            send_mail(email)
        elif self.status =='Declined' and 'status' in self.get_dirty_fields():
            email = {
                'to': 'wphukungoane@gmail.com',
                'cc': 'wphukungoane@gmail.com',
                'subject': 'Project User {} {} has been activated',
                'message': '{} {} has been activated by IT and is ready to use Collab',
            }
            send_mail(email)
