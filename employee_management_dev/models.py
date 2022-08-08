from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class GeneralNotes(models.Model):
    notes = models.CharField(max_length=2000, null=True)
    modified_date = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return f"{self.notes}:{self.modified_date}"


class LocationForWorking(models.Model):
    location_name = models.CharField(max_length=100, null=True)
    notes = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.location_name}"


class LocationForWorkingClone(models.Model):
    location_name = models.CharField(max_length=100, null=True)
    notes = models.CharField(max_length=500, null=True, blank=True)
    custom_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.location_name}"


class EmployeeBaseInformation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    place = models.ForeignKey(
        LocationForWorking, on_delete=models.CASCADE, db_constraint=False, null=True
    )
    phone_number = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    salary = models.IntegerField(null=True)
    bonus = models.IntegerField(null=True)
    is_driver = models.BooleanField(null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}:{self.last_name}"


class EmployeeBaseInformationClone(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    place = models.ForeignKey(
        LocationForWorking, on_delete=models.CASCADE, db_constraint=False, null=True
    )
    phone_number = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    salary = models.IntegerField(null=True)
    bonus = models.IntegerField(null=True)
    is_driver = models.BooleanField(null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    custom_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.first_name}:{self.last_name}"


class WeeklyCalendarFromLocation(models.Model):
    location_place = models.ForeignKey(
        LocationForWorking, on_delete=models.CASCADE, db_constraint=False, null=True
    )
    start_date_week = models.DateField(null=True)

    def __str__(self):
        return f"{self.location_place}:{self.start_date_week}"


class WeeklyCalendarFromLocationClone(models.Model):
    location_place = models.ForeignKey(
        LocationForWorking, on_delete=models.CASCADE, db_constraint=False, null=True
    )
    start_date_week = models.DateField(null=True)
    custom_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.location_place}:{self.start_date_week}"


class WeeklyHoursForEachEmployeeAndLocation(models.Model):
    specific_weekly_calendar = models.ForeignKey(
        WeeklyCalendarFromLocation, on_delete=models.CASCADE
    )
    specific_employee_working = models.ForeignKey(
        EmployeeBaseInformation, on_delete=models.CASCADE
    )
    monday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    tuesday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    wednesday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    thursday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    friday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    saturday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    sunday_num_hours = models.PositiveIntegerField(
        null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(15)]
    )

    # DO NOT CHANGE,  IF SO CHECK VIEWS LST.APPEND IN VIEW_LOCATION
    def __str__(self):
        return f"{self.specific_employee_working.first_name}:{self.specific_weekly_calendar}\n\n\n\t\t\t:{self.monday_num_hours}:{self.tuesday_num_hours}:{self.wednesday_num_hours}:{self.thursday_num_hours}:{self.friday_num_hours}:{self.saturday_num_hours}:{self.sunday_num_hours}"
