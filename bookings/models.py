# bookings/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class CustomUser(AbstractUser):
    """Custom user model for hotel management system"""

    ADMIN = "admin"
    MANAGER = "manager"
    TEAM = "team"
    CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (TEAM, "Team"),
        (CUSTOMER, "Customer"),
    ]

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=CUSTOMER, verbose_name=_("Role")
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name=_("Phone Number"))
    address = models.TextField(blank=True, verbose_name=_("Address"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class GalleryImage(models.Model):
    """Model for hotel images"""

    image = ProcessedImageField(
        upload_to="gallery/",
        processors=[ResizeToFit(1920, 1080)],
        format="JPEG",
        options={"quality": 85},
        verbose_name=_("Image"),
    )
    thumbnail = ProcessedImageField(
        upload_to="gallery/thumbnails/",
        processors=[ResizeToFit(300, 300)],
        format="JPEG",
        options={"quality": 80},
        verbose_name=_("Thumbnail"),
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=100, blank=True, verbose_name=_("Title"))
    room = models.ForeignKey(
        "Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="images",
        verbose_name=_("Room"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Primary Image"))
    upload_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("Upload Date")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Gallery Image")
        verbose_name_plural = _("Gallery Images")
        ordering = ["order", "-upload_date"]

    def __str__(self):
        return f"{self.title or 'Image'} - {self.upload_date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if self.image and not self.thumbnail:
            self.thumbnail = self.image
        if self.is_primary and self.room:
            # Ensure only one primary image per room
            GalleryImage.objects.filter(room=self.room, is_primary=True).exclude(
                id=self.id
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class Room(models.Model):
    """Model for hotel rooms"""

    ROOM_TYPES = [
        ("single", "Single"),
        ("double", "Double"),
        ("suite", "Suite"),
        ("family", "Family"),
    ]

    BED_TYPES = [
        ("single", "Single Bed"),
        ("double", "Double Bed"),
        ("queen", "Queen Bed"),
        ("king", "King Bed"),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Room Name"))
    room_type = models.CharField(
        max_length=10, choices=ROOM_TYPES, verbose_name=_("Room Type")
    )
    room_number = models.CharField(
        max_length=10, unique=True, verbose_name=_("Room Number")
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name=_("Floor Number")
    )

    bed_type = models.CharField(
        max_length=10, choices=BED_TYPES, default="single", verbose_name=_("Bed Type")
    )

    capacity_adults = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name=_("Adult Capacity"),
    )
    capacity_children = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        verbose_name=_("Children Capacity"),
        default=0,
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Price per Night"),
    )

    has_wifi = models.BooleanField(default=True, verbose_name=_("WiFi Available"))
    has_ac = models.BooleanField(default=True, verbose_name=_("Air Conditioning"))
    has_heating = models.BooleanField(default=True, verbose_name=_("Heating"))

    extra_beds_available = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        verbose_name=_("Extra Beds Available"),
    )

    has_tv = models.BooleanField(default=True, verbose_name=_("TV Available"))
    tv_details = models.CharField(
        max_length=100, blank=True, verbose_name=_("TV Details")
    )

    has_private_bathroom = models.BooleanField(
        default=True, verbose_name=_("Private Bathroom")
    )
    has_bathtub = models.BooleanField(default=False, verbose_name=_("Bathtub"))
    has_shower = models.BooleanField(default=True, verbose_name=_("Shower"))
    has_hairdryer = models.BooleanField(default=True, verbose_name=_("Hair Dryer"))

    has_minibar = models.BooleanField(default=False, verbose_name=_("Minibar"))
    has_safe = models.BooleanField(default=False, verbose_name=_("Safe"))
    has_desk = models.BooleanField(default=True, verbose_name=_("Work Desk"))
    has_wardrobe = models.BooleanField(default=True, verbose_name=_("Wardrobe"))
    has_coffee_maker = models.BooleanField(
        default=False, verbose_name=_("Coffee Maker")
    )

    room_view = models.CharField(
        max_length=100, blank=True, verbose_name=_("Room View")
    )
    has_balcony = models.BooleanField(default=False, verbose_name=_("Balcony"))

    description = models.TextField(verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["room_number"]

    def __str__(self):
        return f"{self.room_number} - {self.name}"

    def get_primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    def get_all_images(self):
        return self.images.all().order_by("order")

    def is_available(self, check_in, check_out):
        return not self.bookings.filter(
            models.Q(check_in__lte=check_out) & models.Q(check_out__gte=check_in),
            status__in=["pending", "confirmed"],
        ).exists()


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="bookings", verbose_name=_("Room")
    )
    guest = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("Guest"),
    )
    check_in = models.DateField(verbose_name=_("Check-in Date"))
    check_out = models.DateField(verbose_name=_("Check-out Date"))
    num_adults = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name=_("Number of Adults"),
    )
    num_children = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=0,
        verbose_name=_("Number of Children"),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Total Price"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )
    special_requests = models.TextField(blank=True, verbose_name=_("Special Requests"))
    booking_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Booking Date")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        ordering = ["-booking_date"]

    def __str__(self):
        return f"Booking {self.id} - {self.room.name} ({self.check_in} to {self.check_out})"

    def save(self, *args, **kwargs):
        if not self.total_price:
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)
