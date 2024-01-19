from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from Booking.models import *
from .models import Room

# Create your views here.


def showAllRooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        account = userAccount.objects.filter(email=request.user.username)
        if account:
            account = account[0]
        data = {"rooms": rooms, "acc": account}
        return render(request, "show_all_rooms.html", data)
    if request.method == "POST":
        room_type = request.POST.get("room_type")
        room_capacity = request.POST.get("room_capacity")
        check_in_date = request.POST.get("check_in_date")
        check_out_date = request.POST.get("check_out_date")

        account = userAccount.objects.filter(email=request.user.username)
        if account:
            account = account[0]
        rooms = Room.objects.all()

        # Filter with room type if provided
        if room_type:
            rooms = rooms.filter(roomType=room_type)
        # Filter with capacity if provided
        if room_capacity:
            rooms = rooms.filter(capacity=room_capacity)

        # Filter by date range (Check in and Check out dates)
        if check_in_date and check_out_date:
            check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d").date()
            booked_rooms = currentBookings.objects.filter(
                checkInDate__lte=check_out_date,
                checkOutDate__gte=check_in_date,
            ).values_list("roomNo", flat=True)
            rooms = rooms.exclude(roomNo__in=booked_rooms)

        data = {
            "rooms": rooms,
            "acc": account,
            "room_type": room_type,
            "room_capacity": room_capacity,
            "check_in_date":check_in_date,
            "check_out_date":check_out_date
        }
        return render(request, "show_all_rooms.html", data)
