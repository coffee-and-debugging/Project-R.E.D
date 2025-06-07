from rest_framework.routers import DefaultRouter
from .views import PatientRequestViewSet, DonationResponseViewSet

router = DefaultRouter()
router.register(r'requests', PatientRequestViewSet, basename='requests')
router.register(r'responses', DonationResponseViewSet, basename='responses')

urlpatterns = router.urls
