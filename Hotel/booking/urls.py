
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

# from django_browser_reload.urls import reload_urls
from .views import *

urlpatterns = [
      path("__reload__/", include("django_browser_reload.urls")),
    

 
]
