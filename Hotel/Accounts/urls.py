from .views import *
from . import views
from django.urls import path

app_name = 'Accounts'

urlpatterns = [
    path('LogIn/', userlogin, name='login'),
    path('LogOut/', userlogout, name='logout'),
    path('SignUp/', userSignup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('Profile/', views.profile.as_view(), name='profile'),
    path('EditProfile/', editProfile, name='edit_profile'),
    path('EditPhoto/', editPhoto, name='edit_photo'),
    path('DeleteProfile/', deleteProfile, name='delete_profile'),
    path('ChangePassword/', change_password, name='change_password'),
    path('ForgotPassword/', forgot_password, name='forgot_password'),
    path('OTPVerification/', otp_verification, name='otp_verification'),
]