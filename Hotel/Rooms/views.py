from django.shortcuts import render
from .models import *

# Create your views here.

def showAllRooms(request):
    rooms = Room.objects.all()
    print(rooms)
    
    return render(request, 'show_all_rooms.html', {'rooms':rooms})