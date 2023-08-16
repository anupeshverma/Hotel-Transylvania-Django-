from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from Accounts.models import userAccount
from Rooms.models import Room

# Create your models here.

class Booking(models.Model):
    roomno = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(userAccount, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    bookingDate = models.DateField(default=timezone.now)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)