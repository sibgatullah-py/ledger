from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, RegisterView, LedgerEntryViewSet

# DefaultRouter is a DRF tool that auto-creates REST URLs.
router = DefaultRouter()# Creating and empty router object.
# viewSets are plugged in the router Object.
'''
For customers, use CustomerViewSet and automatically generate all CRUD URLs.
For entries in the Ledger, use LedgerEntryViewSet and automatically generate all CRUD URLS.
'''
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'entries', LedgerEntryViewSet, basename='entries')


# path is normal Django URL
urlpatterns = [
    path('register/', RegisterView.as_view()), # not a view set
] + router.urls

