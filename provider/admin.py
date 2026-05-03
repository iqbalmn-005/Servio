from django.contrib import admin
from django.db.models import Count, Max, Q

from user.models import Booking
from . import models


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    can_delete = False
    fields = ("user", "service", "date", "time", "status")
    readonly_fields = ("user", "service", "date", "time", "status")
    show_change_link = True
    ordering = ("-date", "-time")


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "Name",
        "email",
        "phone_number",
        "service",
        "total_bookings",
        "active_bookings",
        "completed_bookings",
        "latest_booking_date",
    )
    search_fields = ("Name", "email", "phone_number")
    list_filter = ("service",)
    ordering = ("Name",)
    readonly_fields = (
        "total_bookings",
        "active_bookings",
        "completed_bookings",
        "latest_booking_date",
    )
    inlines = (BookingInline,)

    fieldsets = (
        ("Provider Details", {"fields": ("Name", "email", "phone_number", "service", "password")}),
        (
            "Booking Summary",
            {
                "fields": (
                    "total_bookings",
                    "active_bookings",
                    "completed_bookings",
                    "latest_booking_date",
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            total_bookings_count=Count("booking"),
            active_bookings_count=Count(
                "booking",
                filter=Q(booking__status__in=["accepted", "completion_requested"]),
            ),
            completed_bookings_count=Count("booking", filter=Q(booking__status="completed")),
            latest_booking=Max("booking__date"),
        )

    @admin.display(description="Total Bookings")
    def total_bookings(self, obj):
        return obj.total_bookings_count

    @admin.display(description="Active Bookings")
    def active_bookings(self, obj):
        return obj.active_bookings_count

    @admin.display(description="Completed Bookings")
    def completed_bookings(self, obj):
        return obj.completed_bookings_count

    @admin.display(description="Latest Booking Date")
    def latest_booking_date(self, obj):
        return obj.latest_booking or "-"
