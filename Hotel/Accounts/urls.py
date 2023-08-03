from .views import *
from . import views
from django.urls import path

app_name = 'Accounts'

urlpatterns = [
    path('LogIn/', userlogin, name='login'),
    path('LogOut/', userlogout, name='logout'),
    path('SignUp/', userSignup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('ActivationEmail/', resendActivationEmail, name='resend_activation_email'),
    path('Profile/', views.profile.as_view(), name='profile'),
    path('EditProfile/', editProfile, name='edit_profile'),
    path('EditPhoto/', editPhoto, name='edit_photo'),
    path('DeleteProfile/', deleteProfile, name='delete_profile'),
    path('ChangePassword/', changePassword, name='change_password'),
    path('ForgotPassword/', forgotPassword, name='forgot_password'),
    path('OTPVerification/', otpVerification, name='otp_verification'),
    path('CheckRender/', checkrender, name='check'),
]