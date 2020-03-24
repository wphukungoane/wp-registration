from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse

from .forms import NewProjectForm
from .models import ProjectInfo


# Create your views here.
class projectListView(ListView):
    model = ProjectInfo
    context_object_name = 'projects'
    template_name = 'projects.html'
    paginate_by = 20

@login_required
def new_project(request):
    
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_owner = request.user
            project.save()

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html',{'form':NewProjectForm })
