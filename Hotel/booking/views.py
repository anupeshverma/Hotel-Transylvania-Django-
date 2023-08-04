from django.shortcuts import render
from .models import *

def booking(request, room_type, room_number):
    return render(request, 'booking_form.html', {
        'room_type': room_type,
        'room_number': room_number
    })

def showRooms(request):
    roomData=Room.objects.all()
    roomType=RoomType.objects.all()
    data={'roomData':roomData,
    'roomType':roomType,
    }
    if(request.method=='GET'):
        return render(request, 'show_all_room.html',data)