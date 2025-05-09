"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import hello_world

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/hello/', hello_world),
    # path('api/location/', include('locations.urls')),
    path('api/users/', include('users.urls')),

    # path('locations/', include('locations.urls')),
    # path('users/', include('users.urls')),
    # path('hospitals/', include('hospitals.urls')),
    # path('blood_requests/', include('blood_requests.urls')),
    # path('donations/', include('donations.urls')),
    # path('ml_predictions/', include('ml_predictions.urls')),
    # path('notifications/', include('notifications.urls')),
    # path('chats/', include('chats.urls')),
    # path('admin_control/', include('admin_control.urls')),
    # path('reports/', include('reports.urls')),
]
