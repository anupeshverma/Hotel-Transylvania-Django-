from django.shortcuts import render, redirect
# from Booking.models import Room

def home(request):
    
    return render(request, 'index.html')

