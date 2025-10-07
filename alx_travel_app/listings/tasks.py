from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been confirmed. Thank you for choosing ALX Travel!"
    send_mail(
        subject,
        message,
        "noreply@alxtravel.com",  # sender
        [user_email],             # recipient
        fail_silently=False,
    )
    return f"Email sent to {user_email} for booking {booking_id}"
