from django.urls import path,re_path
from . import views

app_name = 'booking'

urlpatterns = [
    # Add your other URL patterns here...
    path('booking/<str:room_type>/<int:room_number>/', views.booking, name='booking_form'),
    # ...
]
