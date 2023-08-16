from django.db import models
from django.utils import timezone
from Accounts.models import userAccount
from Rooms.models import Room

class Booking(models.Model):
    user = models.ForeignKey(userAccount, on_delete=models.CASCADE, default="")
    roomNo = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)
    guestName = models.CharField(max_length=25, default="")
    roomType = models.CharField(max_length=20, default="General")
    capacity = models.CharField(max_length=25, default="Single")
    bookingDate = models.DateField(default=timezone.now)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()

    def __str__(self):
        return str(self.roomNo) + " " + str(self.guestName)
