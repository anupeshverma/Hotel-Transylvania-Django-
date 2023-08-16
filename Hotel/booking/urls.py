from .views import *
from . import views
from django.urls import path

app_name = 'Booking'

urlpatterns = [
    path('book_room/', bookRoom, name='login'),
]