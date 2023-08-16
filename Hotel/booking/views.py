from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def bookRoom(request):
    return render(request, 'booking_form.html')
