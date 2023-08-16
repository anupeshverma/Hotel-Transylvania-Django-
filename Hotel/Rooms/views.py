from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

def showAllRooms(request):
    rooms = Room.objects.all()
    print(rooms)
    
    return render(request, 'show_all_rooms.html', {'rooms':rooms})

class addRoom(LoginRequiredMixin, View): 
    def get(self, request):
        return render(request, 'add_room.html')
    
    def post(self, request):
        roomNo = request.POST['roomNo']
        roomType = request.POST['roomType']
        capacity = request.POST['roomCapacity']
        price = request.POST['price']
        roomImage = request.FILES.get("roomImage")
        description = request.POST['description']
        
        room = Room(roomNo=roomNo, roomType=roomType, capacity=capacity, price=price, roomImage=roomImage, description=description)

        room.save()
        
        return render(request, 'show_all_rooms.html')