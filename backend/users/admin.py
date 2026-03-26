from django.contrib import admin
from django.utils.html import format_html
from .models import SoilScan, UserProfile

@admin.register(SoilScan)
class SoilScanAdmin(admin.ModelAdmin):
    # This list determines what columns you see in the main table
    list_display = ('soil_type', 'user_name', 'date', 'view_on_map')
    
    # This function creates the clickable link
    def view_on_map(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">📍 Open in Maps</a>', url)
        return "No Location"
    
    view_on_map.short_description = "Google Maps"

admin.site.register(UserProfile)