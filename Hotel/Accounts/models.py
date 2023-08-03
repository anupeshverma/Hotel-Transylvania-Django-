from django.db import models
import os 

def user_profile_pic_path(instance, filename):
    # Get the user's ID
    user_id = instance.id

    # Generate the new filename using the user's ID
    new_filename = f'user_{user_id}{os.path.splitext(filename)[1]}'

    # Return the full path for the file
    return os.path.join('profile_pics', new_filename)

# Create your models here.
class userAccount(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=20, default="Human")
    profile_pic = models.ImageField(upload_to=user_profile_pic_path)

    def __str__(self):
        return self.first_name + " " + self.role
