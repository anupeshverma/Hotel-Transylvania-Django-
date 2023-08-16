from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from Accounts.models import userAccount

# Create your models here.
class Room(models.Model):
    ROOM_TYPE = (
        ('general', 'General'),
        ('special','Special')
        )
    CAPACITY = (
        ('single', 'Single'),
        ('double','Double'),
        ('triple','Triple')
        )
    room_no = models.IntegerField(primary_key=True)
    type  = models.CharField('Room Type', max_length=10, choices=ROOM_TYPE , default='general' )
    capacity = models.CharField('Capacity', max_length=20, choices = CAPACITY)
    price = models.FloatField()

    def __str__(self):
        return self.room_no
    

class Booking(models.Model):
    roomno = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(userAccount, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)