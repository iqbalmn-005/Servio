from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "Name", "email", "phone_number", "address")
    search_fields = ("Name", "email", "phone_number", "address")
    ordering = ("Name",)


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "provider", "service", "date", "time", "status")
    list_filter = ("status", "service", "date")
    search_fields = ("user__Name", "provider__Name", "service")
    ordering = ("-date", "-time")


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__Name", "title", "message")
    ordering = ("-created_at",)
