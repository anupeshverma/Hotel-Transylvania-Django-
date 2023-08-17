from .views import *
from . import views
from django.urls import path

app_name = 'Rooms'

urlpatterns = [
    path('showAllRooms/', showAllRooms, name='show_all_rooms'),
    path('showFilteredRooms/', showFilteredRooms, name='show_filtered_rooms'),
    path('addRoom/', views.addRoom.as_view(), name='add_room'),
]