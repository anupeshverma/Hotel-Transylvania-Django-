from .views import *
from . import views
from django.urls import path

app_name = 'Booking'

urlpatterns = [
    path('bookRoom/', bookRoom, name='book_room'),
   
]