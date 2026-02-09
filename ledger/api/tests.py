from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Customer, LedgerEntry
from datetime import date


class LedgerAPITest(APITestCase):

    def setUp(self):
        # create user
        self.user = User.objects.create_user(username='testuser', password='123456')

        # login and get token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': '123456'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_customer(self):
        response = self.client.post('/app/customers/', {
            'name': 'John Doe',
            'phone': '123456789',
            'address': 'Test Address'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_ledger_entry(self):
        customer = Customer.objects.create(user=self.user, name='Jane', phone='999')

        response = self.client.post('/app/entries/', {
            'customer': customer.id,
            'type': 'credit',
            'amount': '100.00',
            'note': 'Test',
            'entry_date': str(date.today())
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_summary(self):
        customer = Customer.objects.create(user=self.user, name='Jane', phone='999')

        LedgerEntry.objects.create(
            user=self.user,
            customer=customer,
            type='credit',
            amount=200,
            entry_date=date.today()
        )

        LedgerEntry.objects.create(
            user=self.user,
            customer=customer,
            type='debit',
            amount=50,
            entry_date=date.today()
        )

        response = self.client.get(f'/app/customers/{customer.id}/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 150)
