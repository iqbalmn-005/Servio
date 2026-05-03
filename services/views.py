from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from user.models import Booking
from django.db.models import Count
from django.core.paginator import Paginator


def admin_index(request):
    bookings_per_day = Booking.objects.values('date').annotate(count=Count('id')).order_by('date')
    dates = [b['date'].strftime('%Y-%m-%d') for b in bookings_per_day if b['date']]
    counts = [b['count'] for b in bookings_per_day if b['date']]
    
    recent_bookings = Booking.objects.select_related('provider').order_by('-date', '-time')[:5]
    
    return render(request, 'admin_index.html', {'dates': dates, 'counts': counts, 'recent_bookings': recent_bookings})

def admin_login(request):
    return render(request,'admin_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_index')
            else:
                return render(request, 'admin_login.html', {'error': 'Not an admin user'})
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})

    return render(request, 'admin_login.html')

def recent_bookings(request):
    bookings_list = Booking.objects.select_related('provider').order_by('-date', '-time')
    paginator = Paginator(bookings_list, 5) # Show 5 bookings per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_recent.html', {'page_obj': page_obj})

def pending_providers(request):
    from provider.models import Provider
    pending_providers_list = Provider.objects.filter(is_approved=False).order_by('-id')
    return render(request, 'admin_pending_providers.html', {'pending_providers': pending_providers_list})

def approve_provider(request, id):
    from provider.models import Provider
    provider = Provider.objects.get(id=id)
    provider.is_approved = True
    provider.save()
    return redirect('pending_providers')

def reject_provider(request, id):
    from provider.models import Provider
    provider = Provider.objects.get(id=id)
    provider.delete()
    return redirect('pending_providers')

def approved_providers(request):
    from provider.models import Provider
    from django.db.models import Count, Q, Avg
    approved_providers_list = Provider.objects.filter(is_approved=True).annotate(
        received_bookings=Count('booking'),
        pending_bookings=Count('booking', filter=Q(booking__status='pending')),
        accepted_bookings=Count('booking', filter=Q(booking__status='accepted')),
        completed_bookings=Count('booking', filter=Q(booking__status='completed')),
        avg_rating=Avg('reviews__rating')
    ).order_by('-id')
    return render(request, 'admin_approved_providers.html', {'approved_providers': approved_providers_list})

def remove_provider(request, id):
    from provider.models import Provider
    provider = Provider.objects.get(id=id)
    provider.delete()
    return redirect('approved_providers')


def admin_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')