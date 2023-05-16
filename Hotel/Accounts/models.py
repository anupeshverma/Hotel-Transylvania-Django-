from django.db import models

# Create your models here.
class userAccount(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=20, default="Human")
    profile_pic = models.ImageField(upload_to="profile_pics")

    def __str__(self):
        return self.first_name + " " + self.role
