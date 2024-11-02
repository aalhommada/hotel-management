from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model for hotel management system"""
    ADMIN = 'admin'
    MANAGER = 'manager'
    TEAM = 'team'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (TEAM, 'Team'),
        (CUSTOMER, 'Customer'),
    ]
    
    # Add related_name to avoid clash with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',  # Changed this
        related_query_name='custom_user'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',  # Changed this
        related_query_name='custom_user'
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        verbose_name=_('Role')
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Phone Number')
    )
    address = models.TextField(
        blank=True,
        verbose_name=_('Address')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Room(models.Model):
    """Model for hotel rooms"""
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('family', 'Family'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Room Name')
    )
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPES,
        verbose_name=_('Room Type')
    )
    capacity_adults = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name=_('Adult Capacity')
    )
    capacity_children = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        verbose_name=_('Children Capacity'),
        default=0
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Price per Night')
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    amenities = models.JSONField(
        default=dict,
        verbose_name=_('Amenities')
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_('Floor Number')
    )
    room_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Room Number')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['room_number']

    def __str__(self):
        return f"{self.room_number} - {self.name}"

    def is_available(self, check_in, check_out):
        """Check if room is available for given dates"""
        return not self.bookings.filter(
            models.Q(check_in__lte=check_out) & 
            models.Q(check_out__gte=check_in),
            status__in=['pending', 'confirmed']
        ).exists()

class Booking(models.Model):
    """Model for room bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_('Room')
    )
    guest = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_('Guest')
    )
    check_in = models.DateField(
        verbose_name=_('Check-in Date')
    )
    check_out = models.DateField(
        verbose_name=_('Check-out Date')
    )
    num_adults = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name=_('Number of Adults')
    )
    num_children = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=0,
        verbose_name=_('Number of Children')
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Total Price')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    special_requests = models.TextField(
        blank=True,
        verbose_name=_('Special Requests')
    )
    booking_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Booking Date')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking {self.id} - {self.room.name} ({self.check_in} to {self.check_out})"

    def save(self, *args, **kwargs):
        if not self.total_price:
            # Calculate number of nights
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

class RoomImage(models.Model):
    """Model for room images"""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Room')
    )
    image = models.ImageField(
        upload_to='room_images/',
        verbose_name=_('Image')
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('Is Primary Image')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    class Meta:
        verbose_name = _('Room Image')
        verbose_name_plural = _('Room Images')
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.room.name}"