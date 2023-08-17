from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from Booking.models import Booking
from .models import Room
# Create your views here.


def showAllRooms(request):
    rooms = Room.objects.all()
    print(rooms)
    
    return render(request, 'show_all_rooms.html', {'rooms':rooms})

# function to show only available rooms 
def  showFilteredRooms(request):
    if request.method == 'POST':
       
        room_capacity = request.POST.get('room_capacity')
        check_in_date = datetime.strptime(request.POST.get('check_in_date'), '%Y-%m-%d').date()
        check_out_date = datetime.strptime(request.POST.get('check_out_date'), '%Y-%m-%d').date()
 
        print(room_capacity)
        print(check_in_date)
        print(check_out_date)
        
        

        # Step 1: Get booked rooms with the specified capacity and overlapping date range
        booked_rooms = Booking.objects.filter(
        capacity=room_capacity,
        checkInDate__lte=check_out_date,
        checkOutDate__gte=check_in_date ).values_list('roomNo', flat=True)
       
 
        
        # Step 2: Get available rooms with the specified capacity
        available_rooms = Room.objects.filter(
            capacity=room_capacity
        ).exclude(roomNo__in=booked_rooms)
       
        print(available_rooms)

        context = {
            'available_rooms': available_rooms,
            'filter_applied': True,  # Set this flag to indicate filter applied
        }

        return render(request, 'show_all_rooms.html', context)


#  function to add room         

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

        # Fetch the list of rooms again
        rooms = Room.objects.all()

        # Pass the rooms to the template
        context = {'rooms': rooms}
        
        return render(request, 'show_all_rooms.html', context)
