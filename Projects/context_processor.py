from .models import ProjectInfo
from datetime import date
from django.contrib.auth.models import User

def project_approved(request):
   return { 'approved_projects' : ProjectInfo.objects.filter(status='Approved').count() }

def project_declined(request):
   return { 'declined_projects' : ProjectInfo.objects.filter(status='Declined').count() }

def project_pending(request):
   return { 'pending_projects' : ProjectInfo.objects.filter(status='Pending').count() }

def project_completed(request):
   return { 'completed_projects' : ProjectInfo.objects.filter(status='Completed').count() }

def new_user_count_month(request):

   return { 'count_by_month' :[User.objects.filter(date_joined__month=x.month).count()
                     for x in User.objects.dates('date_joined','month')] }
