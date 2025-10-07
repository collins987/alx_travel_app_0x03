import os
import requests
from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Payment
from django.conf import settings
from .tasks import send_booking_confirmation_email

CHAPA_SECRET_KEY = settings.CHAPA_SECRET_KEY
CHAPA_BASE_URL = settings.CHAPA_BASE_URL

 # Create your views here.
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email  # assuming Booking has FK to User
        send_booking_confirmation_email.delay(user_email, booking.id)



class InitiatePaymentView(View):
    def post(self, request):
        data = request.POST
        amount = data.get('amount')
        booking_reference = data.get('booking_reference')

        payload = {
            "amount": amount,
            "currency": "ETB",  # Change if needed
            "email": "customer@example.com",  # Ideally from booking/user data
            "first_name": "John",  # Ideally from booking/user data
            "last_name": "Doe",
            "tx_ref": f"{booking_reference}_{os.urandom(4).hex()}",
            "callback_url": "http://localhost:8000/api/verify-payment/"
        }

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"{CHAPA_BASE_URL}/transaction/initialize", json=payload, headers=headers)
        res_data = response.json()

        if res_data.get('status') == 'success':
            Payment.objects.create(
                booking_reference=booking_reference,
                transaction_id=payload['tx_ref'],
                amount=amount,
                status='Pending'
            )
            return JsonResponse({"checkout_url": res_data['data']['checkout_url']})
        else:
            return JsonResponse({"error": res_data}, status=400)


class VerifyPaymentView(View):
    def get(self, request):
        tx_ref = request.GET.get('tx_ref')
        payment = get_object_or_404(Payment, transaction_id=tx_ref)

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        }

        response = requests.get(f"{CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers)
        res_data = response.json()

        if res_data.get('status') == 'success' and res_data['data']['status'] == 'success':
            payment.status = 'Completed'
            payment.save()
            return JsonResponse({"message": "Payment verified successfully"})
        else:
            payment.status = 'Failed'
            payment.save()
            return JsonResponse({"message": "Payment verification failed"}, status=400)
