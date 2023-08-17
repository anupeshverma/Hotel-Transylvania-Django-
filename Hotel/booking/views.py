from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.views import View
from .models import *


# Create your views here.
class bookRoomForm(LoginRequiredMixin, View):
    def get(self, request, capacity, room_number, roomType):
        context = {
            "capacity": capacity,
            "room_number": room_number,
            "room_type": roomType,
        }
        return render(request, "booking_form.html", context)


def bookRoom(request):
    name = request.POST["name"]
    email = request.POST["email"]
    roomNo = request.POST["room_number"]
    roomType = request.POST["room_type"]
    capacity = request.POST["room_capacity"]
    checkIn = request.POST["check_in"]
    checkOut = request.POST["check_out"]

    user_email = request.user
    print(user_email)
    userInstance = get_object_or_404(userAccount, email=user_email)
    roomInstance = get_object_or_404(Room, roomNo=roomNo)
    newBooking = Booking(
        user=userInstance,
        roomNo=roomInstance,
        guestName=name,
        roomType=roomType,
        capacity=capacity,
        checkInDate=checkIn,
        checkOutDate=checkOut,
    )
    currBooking = currentBookings(
        user=userInstance,
        roomNo=roomInstance,
        guestName=name,
        roomType=roomType,
        capacity=capacity,
        checkInDate=checkIn,
        checkOutDate=checkOut,
    )
    newBooking.save()
    currBooking.save()

    # Send email
    message = f"Your booking has been done succesfully.\nHere are the deatils:\nName: {name}\nRoom No.: {roomNo}\nRoom Type: {roomType}\nRoom Capacity: {capacity}\nCheckIn Date: {checkIn}\nCheckOut Date: {checkOut}"
    mail_subject = "Room booked succcesfully"
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.send()
    # if user_email != email:
    #     email = EmailMessage(mail_subject, message, to=[email])
    #     email.send()
    return render(
        request, "error_page.html", {"error": "Hola! Room Booked Successfully."}
    )
