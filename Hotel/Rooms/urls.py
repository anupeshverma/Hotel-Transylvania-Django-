from .views import *
from . import views
from django.urls import path

app_name = 'Rooms'

urlpatterns = [
    path('showAllRooms/', showAllRooms, name='show_all_rooms'),

]