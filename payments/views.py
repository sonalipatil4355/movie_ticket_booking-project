from django.shortcuts import render,redirect
from bookings.models import Booking
from accounts.models import User
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from .models import Payment
# Create your views here.

def Payment_View(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [{
                'price_data':{
                    'currency':'inr',
                    'product_data':{
                        'name':'Ticket Booking',                    
                        },
                        'unit_amount':int(booking.total_amount*100),
                },
                'quantity':1,
            }],
            mode='payment',
            billing_address_collection='required',
            success_url=f'http://127.0.1:8000/payments/success/{booking_id}/',
            cancel_url=f'http://127.0.1:8000/payments/cancel/{booking_id}/',
        )
        return redirect(session.url, code=303)
    return render(request,'bookings/payment.html',{
        'stripe_public_key':settings.STRIPE_PUBLIC_KEY,
        'booking':booking
    })
from django.shortcuts import render, get_object_or_404
from .models import Payment
from bookings.models import Booking

def Success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if payment already exists
    payment_exists = Payment.objects.filter(booking=booking).exists()
    if not payment_exists:
        Payment.objects.create(
            booking=booking,
            transaction_id=f"TXN{booking.id}",  # ensure this is unique
            amount=booking.total_amount,
            status="Success"
        )

    # Get the payment for display
    payment = Payment.objects.get(booking=booking)

    return render(request, 'payments/success.html', {
        'booking': booking,
        'payment': payment,
    })



def Cancel_view(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='Card',
        status = 'failed',
    )
    
    return render(request,'payments/cancel.html')