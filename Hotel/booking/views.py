from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError

# Create your views here.
def bookRoom(request):
    return HttpResponse("BOkk room")