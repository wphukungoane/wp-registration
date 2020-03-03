from django.shortcuts import render
from django.http import HttpResponse

# Index page
def index(request):
    return HttpResponse("Home Page for CHPC registration")
