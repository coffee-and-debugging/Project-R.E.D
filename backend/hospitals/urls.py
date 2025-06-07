from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)

urlpatterns = router.urls
