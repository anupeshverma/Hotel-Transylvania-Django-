from .views import *
from . import views
from django.urls import path

app_name = 'AdminPanel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addUser/', views.addUser.as_view(), name='add_user'),
    path('editUser/<str:userid>', views.editUser.as_view(), name='edit_user'),
    path('deleteUser/<str:userid>', views.deleteUser.as_view(), name='delete_user'),
    path('allUsers/', views.allUsers.as_view(), name='all_users'),
    path('allBookings/', views.allBookings.as_view(), name='all_bookings'),
   
]