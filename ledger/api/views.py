from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Customer, LedgerEntry
from .serializers import *





# User registration endpoint 
class RegisterView(generics.CreateAPIView): # not a viewSet
    queryset = User.objects.all()
    serializer_class = RegisterSerializer




''' 
ViewSet for managing Customer CRUD operations
Only authenticated users can access 
'''
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return only customers belonging to the current user
        return Customer.objects.filter(user=self.request.user) # User Isolation

    def perform_create(self, serializer):
        # Set the user field to the current user on creation
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        Custom endpoint to get a summary of a customer's ledger:
        - total_credit: sum of all credit entries
        - total_debit: sum of all debit entries
        - balance: credit - debit
        """
        customer = self.get_object()

        # Get all ledger entries for this customer and user
        entries = LedgerEntry.objects.filter(user=request.user, customer=customer)

        # sums for credit and debit
        total_credit = entries.filter(type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debit = entries.filter(type='debit').aggregate(Sum('amount'))['amount__sum'] or 0

        balance = total_credit - total_debit

        return Response({
            "total_credit": total_credit,
            "total_debit": total_debit,
            "balance": balance
        })


        
'''
ViewSet for managing ledger entries (credit/debit)
Only authenticated users can access
'''
class LedgerEntryViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return ledger entries for the current user, with optional filtering:
        - by customer (customer query param)
        - by type (credit/debit)
        - by date range (start_date, end_date)
        """
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
        # Setting the user field to the current user on creation
        serializer.save(user=self.request.user)