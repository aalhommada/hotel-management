# Generated by Django 5.1.2 on 2024-11-03 07:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="amenities",
        ),
        migrations.AddField(
            model_name="room",
            name="bed_type",
            field=models.CharField(
                choices=[
                    ("single", "Single Bed"),
                    ("double", "Double Bed"),
                    ("queen", "Queen Bed"),
                    ("king", "King Bed"),
                ],
                default="single",
                max_length=10,
                verbose_name="Bed Type",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="extra_beds_available",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(2),
                ],
                verbose_name="Extra Beds Available",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="has_ac",
            field=models.BooleanField(default=True, verbose_name="Air Conditioning"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_balcony",
            field=models.BooleanField(default=False, verbose_name="Balcony"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_bathtub",
            field=models.BooleanField(default=False, verbose_name="Bathtub"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_coffee_maker",
            field=models.BooleanField(default=False, verbose_name="Coffee Maker"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_desk",
            field=models.BooleanField(default=True, verbose_name="Work Desk"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_hairdryer",
            field=models.BooleanField(default=True, verbose_name="Hair Dryer"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_heating",
            field=models.BooleanField(default=True, verbose_name="Heating"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_minibar",
            field=models.BooleanField(default=False, verbose_name="Minibar"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_private_bathroom",
            field=models.BooleanField(default=True, verbose_name="Private Bathroom"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_safe",
            field=models.BooleanField(default=False, verbose_name="Safe"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_shower",
            field=models.BooleanField(default=True, verbose_name="Shower"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_tv",
            field=models.BooleanField(default=True, verbose_name="TV Available"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_wardrobe",
            field=models.BooleanField(default=True, verbose_name="Wardrobe"),
        ),
        migrations.AddField(
            model_name="room",
            name="has_wifi",
            field=models.BooleanField(default=True, verbose_name="WiFi Available"),
        ),
        migrations.AddField(
            model_name="room",
            name="room_view",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Room View"
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="tv_details",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="TV Details"
            ),
        ),
    ]
