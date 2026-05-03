from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from . import models

class BaseProviderAdmin(admin.ModelAdmin):
    provider_field = None 
    
    def provider_name(self, obj):
        provider = getattr(obj, self.provider_field)
        return provider.Name if provider else "-"
    provider_name.short_description = "Provider Name"
    
    def order_details(self, obj):
        provider = getattr(obj, self.provider_field)
        if not provider:
            return "No Provider Assigned"
        
        bookings = provider.booking_set.all().order_by('-date', '-time')
        if not bookings.exists():
            return "No Orders"
        
        table_html = """
        <table style="width:100%; text-align:left; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">Order ID</th>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">User</th>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">Service</th>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">Date</th>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">Time</th>
                    <th style="border-bottom: 1px solid #ddd; padding: 8px;">Status</th>
                </tr>
            </thead>
            <tbody>
        """
        for b in bookings:
            table_html += f"""
                <tr>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.id}</td>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.user.Name if b.user else '-'}</td>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.service or '-'}</td>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.date}</td>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.time}</td>
                    <td style="border-bottom: 1px solid #ddd; padding: 8px;">{b.status}</td>
                </tr>
            """
        table_html += "</tbody></table>"
        return mark_safe(table_html)
    
    order_details.short_description = "Order Details"

    list_display = ('id', 'provider_name')
    readonly_fields = ('order_details',)

@admin.register(models.AcMechanic)
class AcMechanicAdmin(BaseProviderAdmin):
    provider_field = 'ac_mechanic'

@admin.register(models.Plumbing)
class PlumbingAdmin(BaseProviderAdmin):
    provider_field = 'plumber'

@admin.register(models.Wiring)
class WiringAdmin(BaseProviderAdmin):
    provider_field = 'electrician'
