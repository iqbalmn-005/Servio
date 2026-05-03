from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.user_login,name='user_login'),
    path('register/',views.user_registration,name='user_registration'),
    path('logout/',views.user_logout,name='user_logout'),
    path('logined/',views.user_logined,name='user_logined'),
    path('plumber/<str:service>/',views.plumber_details,name='plumber'),
    path('wiring/<str:service>/',views.wiring_details,name='wiring'),
    path('Ac/<str:service>/',views.Acmech_details,name='Ac'),
    path('single_provider/<int:id>/<str:service>/',views.single_provider,name='single_provider'),
    path('booking/<int:id>/',views.booking,name='booking'),
    path('success_booking/',views.booking_success,name='success_booking'),
    path('booking_status/',views.booking_status,name='booking_status'),
    path('complete_notification/',views.complete_notification,name='complete_notification'),
    path('user-accept-completion/<int:booking_id>/',views.accept_completion,name='user_accept_completion'),
    path('user-reject-completion/<int:booking_id>/',views.reject_completion,name='user_reject_completion'),
    path('submit_review/<int:booking_id>/',views.submit_review,name='submit_review'),
]
