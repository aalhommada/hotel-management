from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("room/<int:room_id>/", views.room_detail, name="room_detail"),
    path("room/<int:room_id>/book/", views.book_room, name="book_room"),
    path(
        "room/<int:room_id>/booked-dates/",
        views.get_booked_dates,
        name="get_booked_dates",
    ),
]
