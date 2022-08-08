from django.contrib import admin
from .models import (
    EmployeeBaseInformation,
    EmployeeBaseInformationClone,
    LocationForWorking,
    LocationForWorkingClone,
    WeeklyCalendarFromLocation,
    WeeklyHoursForEachEmployeeAndLocation,
    GeneralNotes,
)
from .forms import GeneralNotesForm

# Register your models here.
admin.site.register(EmployeeBaseInformation)
admin.site.register(EmployeeBaseInformationClone)
admin.site.register(LocationForWorking)
admin.site.register(LocationForWorkingClone)
admin.site.register(WeeklyCalendarFromLocation)
admin.site.register(WeeklyHoursForEachEmployeeAndLocation)


class GeneralNotesAdminForm(admin.ModelAdmin):
    readonly_fields = ("modified_date",)
    form = GeneralNotesForm


admin.site.register(GeneralNotes, GeneralNotesAdminForm)
