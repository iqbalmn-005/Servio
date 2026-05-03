from urllib import request

from django.shortcuts import render,redirect
from django.contrib import messages

from user.views import booking
from . import models
from services import models as model1
from user import models as user_models
from provider import models as provider_models
from django.http import HttpResponse
from django.db.models import Q

import provider

# Create your views here.
def provider_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if provider_models.Provider.objects.filter(email=email).exists():
            provider=provider_models.Provider.objects.get(email=email)
            if provider.password==password:
                if not provider.is_approved:
                    return render(request,'provider_login.html',{'error':'Your account is pending admin verification. Please try again later.'})
                request.session['provider_email'] = provider.email
                return redirect('provider_dashboard')
            else:
                return render(request,'provider_login.html',{'error':'Incorrect password'})
        else:
            return render(request,'provider_login.html',{'error':'Invalid email or password'})
    return render(request,'provider_login.html')

def provider_registration(request):
    if request.method=='POST':
        userame=request.POST.get('Name')
        phone_number=request.POST.get('phone_number')
        service_choice=request.POST.get('service')
        email=request.POST.get('email')
        password=request.POST.get('password')
        photo=request.FILES.get('photo')
        if models.Provider.objects.filter(email=email).exists():
           return render(request,'provider_registration.html',{'error':'Email already exists'})
        user=models.Provider(Name=userame,phone_number=phone_number,email=email,service=service_choice,password=password,photo=photo)
        user.save()
        if service_choice=='plumbing':
            user1=model1.Plumbing.objects.create(plumber=user)
            user1.save()
        elif service_choice=='wiring':
            user1=model1.Wiring.objects.create(electrician=user)
            user1.save()
        elif service_choice=='ac':
            user1=model1.AcMechanic.objects.create(ac_mechanic=user)
            user1.save()
        messages.success(request, 'Registration successful! Please wait for admin verification before logging in.')
        return redirect('provider_login')
    return render(request,'provider_registration.html')


def provider_dashboard(request):
    email = request.session.get('provider_email')
    if not email:
        return redirect('provider_login')

    provider = models.Provider.objects.filter(email=email).first()
    if not provider:
        return redirect('provider_login')

    bookings = user_models.Booking.objects.filter(provider=provider).select_related('user')
    incoming_bookings = bookings.filter(Q(status='pending') | Q(status='Pending'))
    active_bookings = bookings.filter(
        Q(status='accepted') |
        Q(status='Accepted') |
        Q(status='completion_requested')
    )
    completed_bookings = bookings.filter(Q(status='completed') | Q(status='Completed'))

    return render(
        request,
        'provider_dashboard.html',
        {
            'provider': provider,
            'incoming_bookings': incoming_bookings,
            'active_bookings': active_bookings,
            'completed_bookings': completed_bookings,
        }
    )

def accepted_jobs(request,id):
    booking = user_models.Booking.objects.filter(id=id).select_related('user', 'provider').first()
    if not booking:
        return redirect('provider_dashboard')

    already_assigned = user_models.Booking.objects.filter(
        provider=booking.provider,
        date=booking.date,
        time=booking.time,
        status__in=['accepted', 'Accepted', 'completion_requested', 'completed', 'Completed']
    ).exclude(id=booking.id).exists()
    if already_assigned:
        booking.status = "cancelled"
        booking.save()
        user_models.UserNotification.objects.create(
            user=booking.user,
            booking=booking,
            title="Booking Rejected",
            message=(
                f"Your booking for {booking.time} on {booking.date} was rejected "
                "because this slot is no longer available."
            )
        )
        return redirect('provider_dashboard')

    booking.status = "accepted"
    booking.save()
    user_models.UserNotification.objects.create(
        user=booking.user,
        booking=booking,
        title="Booking Accepted",
        message=f"{booking.provider.Name} accepted your booking for {booking.time} on {booking.date}."
    )

    same_slot_bookings = user_models.Booking.objects.filter(
        provider=booking.provider,
        date=booking.date,
        time=booking.time,
        status__in=['pending', 'Pending', 'accepted', 'Accepted', 'completion_requested']
    ).exclude(id=booking.id)

    for rejected_booking in same_slot_bookings:
        rejected_booking.status = "cancelled"
        rejected_booking.save()
        user_models.UserNotification.objects.create(
            user=rejected_booking.user,
            booking=rejected_booking,
            title="Booking Rejected",
            message=(
                f"Your booking for {rejected_booking.time} on {rejected_booking.date} was rejected "
                "because this slot has been assigned to another customer."
            )
        )

    return redirect('provider_dashboard')

def reject_job(request,id):
    booking = user_models.Booking.objects.filter(id=id).select_related('user', 'provider').first()
    if booking:
        booking.status = "cancelled"
        booking.save()
        user_models.UserNotification.objects.create(
            user=booking.user,
            booking=booking,
            title="Booking Rejected",
            message=f"{booking.provider.Name} rejected your booking for {booking.time} on {booking.date}."
        )
    return redirect('provider_dashboard')

def complete_job(request,id):
    # provider = provider_models.Provider.objects.get(id=provider_id)
    booking = user_models.Booking.objects.filter(id=id).first()
    booking.status = "completed"
    booking.save()
    
    return redirect('provider_dashboard')

def complete_job_request(request, booking_id):
    booking = user_models.Booking.objects.filter(id=booking_id).select_related('user', 'provider').first()
    if booking:
        booking.status = "completion_requested"
        booking.save()
        user_models.UserNotification.objects.create(
            user=booking.user,
            booking=booking,
            title="Completion Verification Needed",
            message=f"{booking.provider.Name} marked your job as completed. Please verify it."
        )
    return redirect('provider_dashboard')

def user_dashboard(request):
    user = request.user
    bookings = user_models.Booking.objects.filter(user=user)

    return render(request, 'user_dashboard.html', {
        'bookings': bookings
    })

def accept_completion(request, booking_id):
    booking = user_models.Booking.objects.get(id=booking_id)
    booking.status = "completed"
    booking.save()
    return redirect('user_dashboard')


def reject_completion(request, booking_id):
    booking = user_models.Booking.objects.get(id=booking_id)
    booking.status = "accepted"
    booking.save()
    return redirect('user_dashboard')

def logout(request):
    request.session.flush()
    return redirect('index')