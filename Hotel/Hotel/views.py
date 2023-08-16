from django.shortcuts import render, redirect
<<<<<<< HEAD
from booking.models import *


=======
from Booking.models import Room
>>>>>>> a56cc987c97102de83310454f5252a4e30e46011
def home(request):
    roomData=Room.objects.all()
    roomType=RoomType.objects.all()
    data={'roomData':roomData,
    'roomType':roomType,
    }

    return render(request, 'index.html',data)

