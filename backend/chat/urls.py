# chat/urls.py (Updated)
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='chatrooms')

urlpatterns = router.urls