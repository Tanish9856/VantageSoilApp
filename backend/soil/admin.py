from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from soil.models import SoilScan, UserProfile


# Show SoilScans inline under each user
class SoilScanInline(admin.TabularInline):
    model = SoilScan
    extra = 0
    readonly_fields = ('soil_type', 'ph_value', 'moisture', 'crop', 'date', 'image')
    fields = ('soil_type', 'ph_value', 'moisture', 'crop', 'date', 'image')
    can_delete = False
    show_change_link = True


# Show UserProfile (city, mobile) inline under each user
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile (City & Mobile)'
    fields = ('mobile', 'city')


# Extend the default UserAdmin
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


# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(SoilScan)
class SoilScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'soil_type', 'ph_value', 'moisture', 'date')
    list_filter = ('soil_type', 'date')
    search_fields = ('user__username', 'soil_type')
    readonly_fields = ('date',)