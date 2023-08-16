from django.db import models
import os

# Create your models here.
def room_image_path(instance, filename):
    # Get the user's ID
    room_id = instance.roomNo

    # Generate the new filename using the user's ID
    new_filename = f'Room_{room_id}{os.path.splitext(filename)[1]}'

    return f'Room_Images/{instance.capacity}_{instance.roomNo}/{new_filename}'

class Room(models.Model):
    ROOM_TYPE = (
        ('General', 'General'),
        ('Special','Special')
        )
    CAPACITY = (
        ('Single', 'Single'),
        ('Double','Double'),
        ('Triple','Triple')
        )
    roomNo = models.IntegerField(primary_key=True)
    roomType  = models.CharField('Room Type', max_length=20, choices=ROOM_TYPE , default='general' )
    capacity = models.CharField('Capacity', max_length=20, choices = CAPACITY)
    price = models.FloatField()
    roomImage = models.ImageField(upload_to=room_image_path)
    description = models.CharField(max_length=200, default="")
    

    def __str__(self):
        return str(self.capacity) + "_" + str(self.roomNo)
