from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def yes(request):
    return HttpResponse("<h1>yes</h1>")
