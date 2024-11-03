from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from django.apps import AppConfig

from .models import CustomUser, Room, Booking, GalleryImage

# Unregister the default Group admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Update the admin site title and header
admin.site.site_header = "Hotel Management System"
admin.site.site_title = "Hotel Management"
admin.site.index_title = "Hotel Administration"


class RoomImagesInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ["image", "title", "is_primary", "order"]
    classes = ["collapse"]


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name",)}),
        ("Permissions", {"fields": ("permissions",), "classes": ("collapse",)}),
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ["thumbnail_preview", "title", "room", "is_primary", "upload_date"]
    list_filter = ["is_primary", "upload_date", "room"]
    search_fields = ["title", "room__name"]

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;"/>',
                obj.thumbnail.url,
            )
        return ""

    thumbnail_preview.short_description = "Preview"

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = ("username", "email", "role", "phone", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone", "address")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "role"),
            },
        ),
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = [
        "room_number",
        "name",
        "room_type",
        "price_per_night",
        "primary_image_preview",
        "is_active",
    ]
    list_filter = ["room_type", "is_active", "floor"]
    search_fields = ["name", "room_number"]
    inlines = [RoomImagesInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "room_number", "room_type", "floor", "description")},
        ),
        (
            "Capacity and Pricing",
            {"fields": ("capacity_adults", "capacity_children", "price_per_night")},
        ),
        ("Bed Configuration", {"fields": ("bed_type", "extra_beds_available")}),
        ("Basic Amenities", {"fields": ("has_wifi", "has_ac", "has_heating")}),
        ("Entertainment", {"fields": ("has_tv", "tv_details")}),
        (
            "Bathroom",
            {
                "fields": (
                    "has_private_bathroom",
                    "has_bathtub",
                    "has_shower",
                    "has_hairdryer",
                )
            },
        ),
        (
            "Additional Amenities",
            {
                "fields": (
                    "has_minibar",
                    "has_safe",
                    "has_desk",
                    "has_wardrobe",
                    "has_coffee_maker",
                )
            },
        ),
        ("View and Location", {"fields": ("room_view", "has_balcony")}),
        ("Status", {"fields": ("is_active",)}),
    )

    def primary_image_preview(self, obj):
        primary_image = obj.get_primary_image()
        if primary_image and primary_image.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;"/>',
                primary_image.thumbnail.url,
            )
        return ""

    primary_image_preview.short_description = "Primary Image"

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = (
        "id",
        "room",
        "guest",
        "check_in",
        "check_out",
        "status",
        "total_price",
    )
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("room__name", "guest__email", "guest__username")
    ordering = ("-booking_date",)
    readonly_fields = ("booking_date", "total_price")

    fieldsets = (
        ("Booking Information", {"fields": ("room", "guest", "status")}),
        ("Dates", {"fields": ("check_in", "check_out", "booking_date")}),
        (
            "Guest Details",
            {"fields": ("num_adults", "num_children", "special_requests")},
        ),
        ("Payment", {"fields": ("total_price",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == CustomUser.ADMIN:
            return qs
        elif request.user.role == CustomUser.TEAM:
            return qs.filter(status__in=["pending", "confirmed"])
        return qs.filter(guest=request.user)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"


# Update the app config


class BookingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookings"
    verbose_name = "Hotel Management"
