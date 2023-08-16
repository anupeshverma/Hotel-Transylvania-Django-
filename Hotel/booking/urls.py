from .views import *
from . import views
from django.urls import path

app_name = 'Booking'

urlpatterns = [
<<<<<<< HEAD
    # Add your other URL patterns here...
    path('booking/<str:room_type>/<int:room_number>/', views.booking, name='booking_form'),
    path('showRooms/', views.showRooms, name='showRooms'),
    # ...
]
=======
    path('book_room/', bookRoom, name='login'),
]
>>>>>>> a56cc987c97102de83310454f5252a4e30e46011
