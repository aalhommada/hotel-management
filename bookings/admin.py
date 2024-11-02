# bookings/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import CustomUser, Room, Booking, RoomImage

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('room_number', 'name', 'room_type', 'price_per_night', 'capacity_display', 'is_active')
    list_filter = ('room_type', 'is_active', 'floor')
    search_fields = ('name', 'room_number', 'description')
    ordering = ('room_number',)
    
    def capacity_display(self, obj):
        return f"Adults: {obj.capacity_adults}, Children: {obj.capacity_children}"
    capacity_display.short_description = "Capacity"

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'room_number', 'room_type', 'floor')
        }),
        ('Capacity & Pricing', {
            'fields': ('capacity_adults', 'capacity_children', 'price_per_night')
        }),
        ('Details', {
            'fields': ('description', 'amenities', 'is_active')
        }),
    )

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('id', 'room', 'guest', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('room__name', 'guest__email', 'guest__username')
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date', 'total_price')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('room', 'guest', 'status')
        }),
        ('Dates', {
            'fields': ('check_in', 'check_out', 'booking_date')
        }),
        ('Guest Details', {
            'fields': ('num_adults', 'num_children', 'special_requests')
        }),
        ('Payment', {
            'fields': ('total_price',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == CustomUser.MANAGER:
            return qs
        elif request.user.role == CustomUser.TEAM:
            return qs.filter(status__in=['pending', 'confirmed'])
        return qs.filter(guest=request.user)

@admin.register(RoomImage)
class RoomImageAdmin(ModelAdmin):
    list_display = ('room', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('room__name', 'room__room_number')
    ordering = ('-is_primary', '-created_at')
    
    fieldsets = (
        ('Image Information', {
            'fields': ('room', 'image', 'is_primary')
        }),
    )