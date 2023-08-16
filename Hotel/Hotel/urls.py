
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings

# from django_browser_reload.urls import reload_urls
from .views import *

urlpatterns = [
      path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('', home, name ='home'),
    # path('Accounts/', include('Accounts.urls', namespace='Accounts')),
    path('account/', include(('Accounts.urls', 'Accounts'), namespace='Accounts')),
<<<<<<< HEAD
    path('booking/', include(('booking.urls', 'booking'), namespace='booking')),
    #  path('booking/showRooms/', views.showRooms, name='showRooms'),
=======
    path('booking/', include(('Booking.urls', 'Booking'), namespace='Booking')),
>>>>>>> a56cc987c97102de83310454f5252a4e30e46011
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
