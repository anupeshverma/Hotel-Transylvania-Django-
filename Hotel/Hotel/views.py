from django.shortcuts import render, redirect
from Rooms.models import Room


def home(request):
    roomData = Room.objects.all()

    data = {"roomData": roomData}

    return render(request, "index.html", {"roomData": roomData})


def about(request):
    
    return render(request, "about.html")