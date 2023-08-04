from django.db import models

# Create your models here.

# model for room category and type 


def get_room_type_capacity(instance,filename):
    return f'room_images/{instance.type}/{filename}'

class RoomType(models.Model):
    image=models.ImageField(upload_to=get_room_type_capacity)
    TYPE_CHOICE=[
        ('Special','Special'),
        ('General','General')
    ]
    CAPACITY_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]
    
    ROLE=[
        ('Human','Human'),
        ('Monster','Monster'),
        ('Human&Monster','Human&Monster'),
    ]

    type=models.CharField(max_length=10,choices=TYPE_CHOICE)
    capacity=models.CharField(max_length=10,choices=CAPACITY_CHOICES)
    ideal_for=models.CharField(max_length=50,choices=ROLE)

    def __str__(self):
        return f"{self.type}_{self.capacity}"
    

# model for fetching each room 
def get_room_image_upload_path(instance, filename):
    return f'room_images/{instance.capacity}/{instance.number}/{filename}'


class Room(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField is used by default for primary keys
    img = models.ImageField(upload_to=get_room_image_upload_path)  
    CAPACITY_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]
    number=models.IntegerField(default=1)
    capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return f"{self.capacity[0].upper()}{self.number} "





 