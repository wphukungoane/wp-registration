from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, TemplateView, ListView, CreateView, DetailView
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import mail
from email.mime.text import MIMEText
from smtplib import SMTPException
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import ProjectInfo
from django.contrib.sites.shortcuts import get_current_site
from formtools.wizard.views import SessionWizardView
from Projects.forms import NewProjectForm,  ComputeResourceForm



@method_decorator(login_required,  name='dispatch')
class ProjectList(ListView):
    model = ProjectInfo
    context_object_name = 'projects'
    template_name = 'projects_list.html'
    paginate_by = 10
    ordering = ['project_code']

    def get_queryset(self):
        """
        Return all projects if user is admin, else return only owned
        """
        user = self.request.user

        if user.is_staff:
            return ProjectInfo.objects.all().order_by('Project_Owner')

        return ProjectInfo.objects.filter(Project_Owner=self.request.user).order_by('project_code')





@method_decorator(login_required, name='dispatch')
class ProjectCreateWizardView(SessionWizardView):
    template_name = 'includes/multiformp.html'
    form_list =  [ NewProjectForm, ComputeResourceForm]

    def dispatch(self, request, *args, **kwargs):
        return super(ProjectCreateWizardView,self).dispatch(request, *args, **kwargs)

    def get_form_instance(self,step):

        return self.instance_dict.get(step, None)

    def get(self, request, *args, **kwargs):

        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)



    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == '0':
            initial.update({'Project_Owner':self.request.user})

        return initial

    def done(self, form_list,  form_dict, **kwargs):


        #you can access form as
        project = form_dict['0']
        obj1 = project.save(commit=False)
        #now set fields from 2nd form
        resource =form_dict['1']
        obj1.Project_Owner = self.request.user
        obj1.Number_CPU = resource.cleaned_data['Number_CPU']
        obj1.Memory_required = resource.cleaned_data['Memory_required']
        obj1.Storage = resource.cleaned_data['Storage']
        obj1.OS_Type = resource.cleaned_data['OS_Type']
        obj1.save()


        connection = mail.get_connection()
        #current_site = get_current_site()
        user = obj1.Project_Owner
        #msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        #msg.send()
        #subject, from_email, to = 'CHPC Cloud - New Project Application', 'no-reply@openstackusers.chpc.ac.za', 'wphukungoane@gmail.com'

        Reviewer_subject, Reviewer_from_email  = 'CHPC Cloud - New Project Application', 'no-reply@openstackusers.chpc.ac.za'
        to_emails = ['wphukungoane@csir.co.za', 'zmtshali@csir.co.za', 'cfortune@csir.co.za', 'nrampyapedi@csir.co.za', 'dthobye@csir.co.za']
        #text_content = 'Thank you for applying to use CHPC OpenStack Cloud platform.'\
        #                'Your Project Application with project number {} is successfully submitted to the CHPC OpenStack Team to be reviewed.\n\n'\
        #                'Please login https:// {} with your account credentials to check status of the # XXX: Project:'

        Reviewer_text_content = 'A new Project Application has been captured on the Openstackusers Database: \n\n'\
                              'Please login https://openstackusers.chpc.ac.za/projects/projects with your account credentials to review the Project'

        #User_email = mail.EmailMessage(subject, text_content, from_email, [to])
        reviewer_email = mail.EmailMessage(Reviewer_subject, Reviewer_text_content, Reviewer_from_email, to_emails)

        # Send the two emails in a single call -
        connection.send_messages([reviewer_email])
        # The connection was already open so send_messages() doesn't close it.
        # We need to manually close the connection.
        connection.close()

        return render (self.request, 'project_creation_done.html', {
                'form_data': [form.cleaned_data for form in form_list],
                #'contact_lists' : ContactList.objects.all()
            })

        return HttpResponse('We have sent you an email, please confirm your email address to complete registration')




@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):

    model = ProjectInfo
    template_name = 'projects_detail.html'
    context_object_name = "project"



    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['projects'] = ProjectInfo.objects.filter(pk=self.kwargs['pk'])

        return context


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(SuccessMessageMixin,UpdateView):

    model = ProjectInfo
    template_name = 'update_project.html'
    fields = [ 'Project_Name','Research_Area','Project_Description', 'status','Approved_by', 'Review']
    success_message = "Project successfully updated!"
