from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from Booking.models import Booking
from .models import Room

# Create your views here.


def showAllRooms(request):
    rooms = Room.objects.all()
    account = userAccount.objects.filter(email=request.user.username)
    account = account[0]
    data = {"rooms": rooms, "acc": account}
    return render(request, "show_all_rooms.html", data)


# function to show only available rooms
def showFilteredRooms(request):
    if request.method == "POST":
        room_capacity = request.POST.get("room_capacity")
        check_in_date = datetime.strptime(
            request.POST.get("check_in_date"), "%Y-%m-%d"
        ).date()
        check_out_date = datetime.strptime(
            request.POST.get("check_out_date"), "%Y-%m-%d"
        ).date()
        # Step 1: Get booked rooms with the specified capacity and overlapping date range
        booked_rooms = Booking.objects.filter(
            capacity=room_capacity,
            checkInDate__lte=check_out_date,
            checkOutDate__gte=check_in_date,
        ).values_list("roomNo", flat=True)

        # Step 2: Get available rooms with the specified capacity
        available_rooms = Room.objects.filter(capacity=room_capacity).exclude(
            roomNo__in=booked_rooms
        )
        context = {
            "rooms": available_rooms,
        }

        return render(request, "show_all_rooms.html", context)
