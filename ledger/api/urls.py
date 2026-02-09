from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, RegisterView, LedgerEntryViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'entries', LedgerEntryViewSet, basename='entries')

urlpatterns = [
    path('register/', RegisterView.as_view()),
] + router.urls

