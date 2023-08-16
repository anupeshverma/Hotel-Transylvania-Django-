from .views import *
from . import views
from django.urls import path

app_name = 'Booking'

urlpatterns = [
    path('bookRoomForm/<str:capacity>/<int:room_number>/<str:roomType>', views.bookRoomForm.as_view(), name='book_room_form'),
    path('bookRoom/', views.bookRoom, name='book_room'),
   
]