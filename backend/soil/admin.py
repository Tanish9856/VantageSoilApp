from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from soil.models import SoilScan, UserProfile

class SoilScanInline(admin.TabularInline):
    model = SoilScan
    extra = 0
    readonly_fields = ('soil_type', 'ph_value', 'moisture', 'crop', 'date', 'image')
    fields = ('soil_type', 'ph_value', 'moisture', 'crop', 'date', 'image')
    can_delete = False
    show_change_link = True

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile (City & Mobile)'
    fields = ('mobile', 'city')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, SoilScanInline)
    list_display = ('username', 'email', 'first_name', 'get_city', 'get_mobile', 'date_joined')

    def get_city(self, obj):
        try:
            return obj.userprofile.city
        except:
            return '-'
    get_city.short_description = 'City'

    def get_mobile(self, obj):
        try:
            return obj.userprofile.mobile
        except:
            return '-'
    get_mobile.short_description = 'Mobile'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(SoilScan)
class SoilScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'soil_type', 'ph_value', 'moisture', 'date', 'open_in_maps')
    list_filter = ('soil_type', 'date')
    search_fields = ('user__username', 'soil_type')
    readonly_fields = ('date', 'open_in_maps')
    fieldsets = (
        ('Scan Info', {
            'fields': ('user', 'user_name', 'image', 'soil_type', 'ph_value', 'moisture', 'crop', 'is_visible', 'date')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'open_in_maps'),
        }),
    )

    def open_in_maps(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<a href="{}" target="_blank" style="'
                'background:#1a5c2a; color:#fff; padding:4px 10px; '
                'border-radius:6px; text-decoration:none; font-size:12px;">'
                '📍 Open in Maps</a>',
                url
            )
        return "No location saved"
    open_in_maps.short_description = 'Open in Maps'