
from urllib import request

from urllib import request

from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth import logout
from services import models as service_models
from user import models
from provider import models as provider_models
from datetime import date

import user
# Create your views here.


def index(request):
    return render(request,'index.html')

def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if models.User.objects.filter(email=email).exists():
            user=models.User.objects.get(email=email)
            if user.password==password:
                request.session['user'] = user.email
                return redirect('user_logined')
            else:
                return render(request,'user_login.html',{'error':'Incorrect password'})
        else:
            return render(request,'user_login.html',{'error':'Invalid email or password'})
    return render(request,'user_login.html')

def user_registration(request):
    if request.method=='POST':
        userame=request.POST.get('Name')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        address=request.POST.get('address')
        password=request.POST.get('password')
        if models.User.objects.filter(email=email).exists():
           return render(request,'user_registration.html',{'error':'Email already exists'})
        user=models.User(Name=userame,phone_number=phone_number,email=email,address=address,password=password)
        user.save()
        return redirect('index')
    return render(request,'user_registration.html')

def user_logined(request):
    user = request.session.get('user')
    email = models.User.objects.get(email=user)
    return render(request,'user_logined.html',{'user':email})

def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('index')

def plumber_details(request,service):
    from django.db.models import Avg
    plumbers=service_models.Plumbing.objects.filter(plumber__is_approved=True).annotate(
        avg_rating=Avg('plumber__reviews__rating')
    )
    service=service
    return render(request,'plumber_details.html',{'providers':plumbers,'service':service})

def wiring_details(request,service):
    from django.db.models import Avg
    wiring=service_models.Wiring.objects.filter(electrician__is_approved=True).annotate(
        avg_rating=Avg('electrician__reviews__rating')
    )
    service=service
    return render(request,'wiring_details.html',{'providers':wiring,'service':service})

def Acmech_details(request,service):
    from django.db.models import Avg
    Ac=service_models.AcMechanic.objects.filter(ac_mechanic__is_approved=True).annotate(
        avg_rating=Avg('ac_mechanic__reviews__rating')
    )
    service=service
    return render(request,'ac_details.html',{'providers':Ac,'service':service})

def single_provider(request,id,service):
    if service == 'plumbing':
        plumbing = service_models.Plumbing.objects.get(plumber__id=id)
        provider = plumbing.plumber
    elif service=='wiring':
        wiring = service_models.Wiring.objects.get(electrician__id=id)
        provider = wiring.electrician
    elif service=='acmech':
        Ac = service_models.AcMechanic.objects.get(ac_mechanic__id=id)
        provider = Ac.ac_mechanic
    return render(request,'single_provider.html' ,{'provider':provider})


def booking(request, id):
    if request.method == "POST":
        email = request.session.get('user')
        if not email:
            return redirect('user_login')

        user = models.User.objects.get(email=email)
        provider = provider_models.Provider.objects.get(id=id)
        time = request.POST.get('time_slot')
        if not time:
            return render(
                request,
                'single_provider.html',
                {'provider': provider, 'error': 'Please choose a time slot before booking.'}
            )

        today = date.today()
        slot_taken = models.Booking.objects.filter(
            provider=provider,
            date=today,
            time=time,
            status__in=["accepted", "Accepted", "completion_requested", "completed", "Completed"]
        ).exists()
        if slot_taken:
            return render(
                request,
                'single_provider.html',
                {'provider': provider, 'error': 'This time slot is already booked. Please choose another time.'}
            )

        booking = models.Booking(
            user=user,
            provider=provider,
            time=time,
            date=today,
            status="pending"
        )
        booking.save()
        return redirect('success_booking')

def booking_success(request):
    return render(request, 'booking_success.html')

def booking_status(request):
    email = request.session.get('user')
    if not email:
        return redirect('user_login')

    user = models.User.objects.filter(email=email).first()
    if not user:
        return redirect('user_login')

    bookings = models.Booking.objects.filter(user=user).select_related('provider').order_by('-date', '-time')
    return render(
        request,
        'booking_status.html',
        {
            'bookings': bookings,
        }
    )

def complete_notification(request):
    email = request.session.get('user')
    if not email:
        return redirect('user_login')

    user = models.User.objects.filter(email=email).first()
    if not user:
        return redirect('user_login')

    completion_requests = models.Booking.objects.filter(
        user=user,
        status="completion_requested"
    ).select_related('provider')

    # Completed bookings split by whether a review exists — uses DB-level queries
    unreviewed_bookings = models.Booking.objects.filter(
        user=user,
        status='completed'
    ).exclude(
        review__isnull=False
    ).select_related('provider').order_by('-created_at')

    reviewed_bookings = models.Booking.objects.filter(
        user=user,
        status='completed',
        review__isnull=False
    ).select_related('provider', 'review').order_by('-created_at')

    notifications = models.UserNotification.objects.filter(user=user).select_related('booking')
    return render(
        request,
        'complete_notification.html',
        {
            'completion_requests': completion_requests,
            'notifications': notifications,
            'unreviewed_bookings': unreviewed_bookings,
            'reviewed_bookings': reviewed_bookings,
        }
    )

def accept_completion(request, booking_id):
    email = request.session.get('user')
    if not email:
        return redirect('user_login')

    user = models.User.objects.filter(email=email).first()
    if not user:
        return redirect('user_login')

    booking = models.Booking.objects.filter(
        id=booking_id,
        user=user,
        status="completion_requested"
    ).first()
    if booking:
        booking.status = "completed"
        booking.save()

        # Handle review if provided in the POST request
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '')
            if rating:
                models.Review.objects.create(
                    booking=booking,
                    user=user,
                    provider=booking.provider,
                    rating=int(rating),
                    comment=comment
                )

        models.UserNotification.objects.create(
            user=booking.user,
            booking=booking,
            title="Job Completed ✅",
            message=f"You confirmed completion for {booking.provider.Name}. Thank you for your feedback!"
        )
    return redirect('complete_notification')

def reject_completion(request, booking_id):
    email = request.session.get('user')
    if not email:
        return redirect('user_login')

    user = models.User.objects.filter(email=email).first()
    if not user:
        return redirect('user_login')

    booking = models.Booking.objects.filter(
        id=booking_id,
        user=user,
        status="completion_requested"
    ).first()
    if booking:
        booking.status = "accepted"
        booking.save()
        models.UserNotification.objects.create(
            user=booking.user,
            booking=booking,
            title="Completion Rejected",
            message=f"You marked the job with {booking.provider.Name} as not completed yet."
        )
    return redirect('complete_notification')

def submit_review(request, booking_id):
    # This view is now integrated into accept_completion
    return redirect('complete_notification')
