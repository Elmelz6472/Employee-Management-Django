from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


from .models import (
    EmployeeBaseInformation,
    LocationForWorking,
    WeeklyCalendarFromLocation,
    WeeklyHoursForEachEmployeeAndLocation,
    GeneralNotes,
)


class RFPAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "span2", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "span2", "placeholder": "Password"})
    )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmployeeBaseInformationForm(forms.ModelForm):
    class Meta:
        model = EmployeeBaseInformation
        fields = (
            "first_name",
            "last_name",
            "place",
            "phone_number",
            "start_date",
            "salary",
            "bonus",
            "is_driver",
            "notes",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "mx-auto text-center form-control d-flex justify-content-center"
                }
            ),
            "last_name": forms.TextInput(attrs={"class": "text-center form-control"}),
            "place": forms.Select(attrs={"class": "text-center form-control"}),
            "phone_number": forms.TextInput(
                attrs={"class": "text-center form-control"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "text-center form-control", "type": "date"}
            ),
            "salary": forms.TextInput(attrs={"class": "text-center form-control"}),
            "bonus": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "is_driver": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "quick notes..."}
            ),
        }


class LocationForWorkingForm(forms.ModelForm):
    class Meta:
        model = LocationForWorking
        fields = ("location_name", "notes")
        widgets = {
            "location_name": forms.TextInput(
                attrs={"class": "text-center form-control"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "quick notes..."}
            ),
        }


class WeeklyCalendarFromLocationForm(forms.ModelForm):
    class Meta:
        model = WeeklyCalendarFromLocation
        fields = ("location_place", "start_date_week")
        widgets = {
            "location_place": forms.Select(attrs={"class": "text-center form-control"}),
            "start_date_week": forms.DateInput(
                attrs={"class": "text-center form-control", "type": "date"}
            ),
        }


class WeeklyHoursForEachEmployeeAndLocationForm(forms.ModelForm):
    class Meta:
        model = WeeklyHoursForEachEmployeeAndLocation
        fields = (
            "specific_weekly_calendar",
            "specific_employee_working",
            "monday_num_hours",
            "tuesday_num_hours",
            "wednesday_num_hours",
            "thursday_num_hours",
            "friday_num_hours",
            "saturday_num_hours",
            "sunday_num_hours",
        )

        widgets = {
            "specific_weekly_calendar": forms.Select(
                attrs={"class": "text-center form-control"}
            ),
            "specific_employee_working": forms.Select(
                attrs={"class": "text-center form-control"}
            ),
            "monday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "tuesday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "wednesday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "thursday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "friday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "saturday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
            "sunday_num_hours": forms.TextInput(
                attrs={"class": "text-center form-control", "value": "0"}
            ),
        }


class GeneralNotesForm(forms.ModelForm):
    class Meta:
        model = GeneralNotes
        fields = ("notes",)
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "25",
                    "placeholder": "quick notes...",
                }
            ),
        }
