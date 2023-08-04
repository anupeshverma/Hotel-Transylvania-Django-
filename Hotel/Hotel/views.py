from django.shortcuts import render, redirect
from booking.models import *


def home(request):
    roomData=Room.objects.all()
    roomType=RoomType.objects.all()
    data={'roomData':roomData,
    'roomType':roomType,
    }

    return render(request, 'index.html',data)

