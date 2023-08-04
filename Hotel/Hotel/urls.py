
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
    path('booking/', include(('booking.urls', 'booking'), namespace='booking')),
    #  path('booking/showRooms/', views.showRooms, name='showRooms'),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
