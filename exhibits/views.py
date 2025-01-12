from django.shortcuts import render
from django.http import HttpResponse

def exhibits(request):
    return HttpResponse("Hello world!")