from django.db import models

# Create your models here.


class Room(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField is used by default for primary keys
    img = models.ImageField(upload_to='room_images/')  
    CAPACITY_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]
    capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return f"Room {self.id}"
 