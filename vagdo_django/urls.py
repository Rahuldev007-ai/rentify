from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-site/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('user_accounts.urls')),
    path('vehicles/', include('vehicle_rentals.urls')),
    path('properties/', include('property_rentals.urls')),
    path('bookings/', include('booking_manager.urls')),
    path('admin-portal/', include('admin_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
