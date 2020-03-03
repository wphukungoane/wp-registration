from django.shortcuts import render
from django.http import HttpResponse

# Index Page
def index(request):
    return render(request, 'registration/index.html', {})


# Registration Page
def registration(request):
    return render(request, 'registration/registration.html', {})
