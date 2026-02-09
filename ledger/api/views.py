from rest_framework import generics, viewsets, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

from .models import Customer, LedgerEntry
from .serializers import *


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
class LedgerEntryViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LedgerEntry.objects.filter(user=self.request.user)

        customer_id = self.request.query_params.get('customer')
        entry_type = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        if entry_type:
            queryset = queryset.filter(type=entry_type)

        if start_date and end_date:
            queryset = queryset.filter(entry_date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)