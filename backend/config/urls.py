# config/urls.py (Updated)
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", lambda request: HttpResponse("Project-RED Blood Donation System")),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/blood/', include('blood.urls')),
    path('api/hospitals/', include('hospitals.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/gamification/', include('gamification.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)