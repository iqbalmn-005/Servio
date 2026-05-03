from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('provider_login/',views.provider_login,name='provider_login'),
    path('provider_registration/',views.provider_registration,name='provider_registration'),
    path('provider_dashboard/',views.provider_dashboard,name='provider_dashboard'),
    path('reject_job/<int:id>/',views.reject_job,name='reject_job'),
    path('accepted_jobs/<int:id>/',views.accepted_jobs,name='accepted_jobs'),
    path('complete_job/<int:id>/',views.complete_job,name='complete_job'),
    path('complete_job_request/<int:booking_id>/',views.complete_job_request,name='complete_job_request'),
    path('accept-completion/<int:booking_id>/', views.accept_completion, name='accept_completion'),
    path('reject-completion/<int:booking_id>/', views.reject_completion, name='reject_completion'),
    path('logout/',views.logout,name='logout'),
]