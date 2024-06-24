# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.
# def game(request):
#     return HttpResponse("Hello world!")
# myapp/views.py
from django.shortcuts import render
from vpython import *

def simulate(request):
    return render(request, 'simulate.html')