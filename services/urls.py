from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin_dashboard/',views.admin_index,name='admin_index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('recent_bookings/',views.recent_bookings,name='recent_bookings'),
    path('pending_providers/',views.pending_providers,name='pending_providers'),
    path('approved_providers/',views.approved_providers,name='approved_providers'),
    path('approve_provider/<int:id>/',views.approve_provider,name='approve_provider'),
    path('reject_provider/<int:id>/',views.reject_provider,name='reject_provider'),
    path('remove_provider/<int:id>/',views.remove_provider,name='remove_provider'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
]