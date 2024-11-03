from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Room
from .forms import RoomFilterForm, BookingForm
from django.utils import timezone
import json
from datetime import timedelta


def home(request):
    form = RoomFilterForm(request.GET or None)
    rooms = Room.objects.filter(is_active=True)

    if form.is_valid():
        check_in = form.cleaned_data["check_in"]
        check_out = form.cleaned_data["check_out"]
        adults = form.cleaned_data["adults"]
        children = form.cleaned_data.get("children", 0)

        # Filter by capacity
        rooms = rooms.filter(
            capacity_adults__gte=adults, capacity_children__gte=children
        )

        # Filter out booked rooms
        unavailable_rooms = Room.objects.filter(
            bookings__check_in__lte=check_out,
            bookings__check_out__gte=check_in,
            bookings__status__in=["pending", "confirmed"],
        )
        rooms = rooms.exclude(id__in=unavailable_rooms.values_list("id", flat=True))

    context = {"form": form, "rooms": rooms, "is_filtered": form.is_valid()}

    if request.htmx:
        return render(request, "bookings/partials/room_list.html", context)
    return render(request, "bookings/home.html", context)


def get_booked_dates(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    # Get all confirmed and pending bookings
    bookings = room.bookings.filter(
        status__in=["pending", "confirmed"],
        check_out__gte=timezone.now().date(),  # Only get current and future bookings
    )

    booked_dates = []
    for booking in bookings:
        current_date = booking.check_in
        while current_date <= booking.check_out:
            booked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    return JsonResponse({"booked_dates": booked_dates})


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = BookingForm(request.GET or None)

    # Get booked dates for initial load
    bookings = room.bookings.filter(
        status__in=["pending", "confirmed"], check_out__gte=timezone.now().date()
    )

    booked_dates = []
    for booking in bookings:
        current_date = booking.check_in
        while current_date <= booking.check_out:
            booked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    context = {
        "room": room,
        "form": form,
        "booked_dates_json": json.dumps(booked_dates),
    }
    return render(request, "bookings/room_detail.html", context)


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if room is available for these dates
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]

            if room.is_available(check_in, check_out):
                booking = form.save(commit=False)
                booking.room = room
                booking.guest = request.user
                booking.save()

                messages.success(request, "Room booked successfully!")
                return redirect("room_detail", room_id=room.id)
            else:
                messages.error(request, "Room is not available for selected dates.")
    else:
        form = BookingForm()

    context = {
        "room": room,
        "form": form,
    }
    return render(request, "bookings/book_room.html", context)
