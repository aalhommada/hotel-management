from django.utils import timezone
from django import forms
from django.utils.translation import gettext_lazy as _
from bookings.models import Booking


class RoomFilterForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
        ),
        required=True,
        label=_("Check-in Date"),
    )
    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
        ),
        required=True,
        label=_("Check-out Date"),
    )
    adults = forms.IntegerField(
        min_value=1,
        max_value=6,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            }
        ),
        label=_("Adults"),
    )
    children = forms.IntegerField(
        min_value=0,
        max_value=4,
        initial=0,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            }
        ),
        label=_("Children"),
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "num_adults",
            "num_children",
            "special_requests",
        ]
        widgets = {
            "check_in": forms.DateInput(
                attrs={
                    "type": "text",  # Changed from 'date' to 'text' for Flatpickr
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "placeholder": "Select check-in date",
                }
            ),
            "check_out": forms.DateInput(
                attrs={
                    "type": "text",  # Changed from 'date' to 'text' for Flatpickr
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "placeholder": "Select check-out date",
                }
            ),
            "num_adults": forms.NumberInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "min": "1",
                    "max": "6",
                }
            ),
            "num_children": forms.NumberInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "min": "0",
                    "max": "4",
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError(
                    "Check-out date must be after check-in date"
                )

            if check_in < timezone.now().date():
                raise forms.ValidationError("Check-in date cannot be in the past")

        return cleaned_data
