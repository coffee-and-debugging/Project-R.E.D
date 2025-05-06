from django.urls import path
from .views import LocationView

urlpatterns = [
    path('test/', LocationView.as_view(), name='location'),
]