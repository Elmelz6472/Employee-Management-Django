import io
import math
import os
import markdown
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.http import FileResponse
from django.contrib.contenttypes.models import ContentType
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import (
    EmployeeBaseInformation,
    EmployeeBaseInformationClone,
    LocationForWorking,
    LocationForWorkingClone,
    WeeklyCalendarFromLocation,
    WeeklyCalendarFromLocationClone,
    WeeklyHoursForEachEmployeeAndLocation,
    GeneralNotes,
)
from .forms import (
    EmployeeBaseInformationForm,
    LocationForWorkingForm,
    WeeklyCalendarFromLocationForm,
    WeeklyHoursForEachEmployeeAndLocationForm,
    GeneralNotesForm,
    NewUserForm,
)
import datetime
from datetime import datetime as DT
from datetime import date
import pytz

LOGIN_URL = "/employee_management/login"


def server_error(request):
    return render(request, "errors/500.html", {})


def custom_page_not_found_view(request):
    return render(request, "errors/404.html", {})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="employee_management/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                    pass
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(
        request=request,
        template_name="employee_management/login.html",
        context={"login_form": form},
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/employee_management/login")


@login_required(login_url=LOGIN_URL)
def home(request):
    data = EmployeeBaseInformation.objects.all()
    number_employee = len(list(EmployeeBaseInformation.objects.all()))
    number_location = len(list(LocationForWorking.objects.all()))

    filename = DT.now().strftime("%B_%d_%Y") + "_employee_backup"
    return render(
        request,
        "employee_management/home.html",
        {
            "data": data,
            "number_employee": number_employee,
            "number_location": number_location,
            "filename": filename
        },
    )


@login_required(login_url=LOGIN_URL)
def submit(request):
    form = EmployeeBaseInformationForm(initial={"start_date": date.today()})

    if request.method == "POST":
        form = EmployeeBaseInformationForm(request.POST)
        if form.is_valid():

            instance = form.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(
                    EmployeeBaseInformation
                ).pk,
                object_id=instance.id,
                object_repr=f"{instance.first_name} {instance.last_name} working at {instance.place}",
                action_flag=ADDITION,
            )

            return redirect("home")
    return render(request, "employee_management/form.html", {"form": form})


@login_required(login_url=LOGIN_URL)
def delete_employee(request, employee_id):
    specific_employee = EmployeeBaseInformation.objects.get(pk=employee_id)
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(EmployeeBaseInformation).pk,
        object_id=specific_employee.id,
        object_repr=f"{specific_employee.first_name} {specific_employee.last_name} working at {specific_employee.place} [Employee]",
        action_flag=DELETION,
    )

    employee_clone = EmployeeBaseInformationClone(
        first_name=specific_employee.first_name,
        last_name=specific_employee.last_name,
        place=specific_employee.place,
        phone_number=specific_employee.phone_number,
        start_date=specific_employee.start_date,
        salary=specific_employee.salary,
        bonus=specific_employee.bonus,
        is_driver=specific_employee.is_driver,
        notes=specific_employee.notes,
        custom_id=specific_employee.id,
    )
    employee_clone.save()

    specific_employee.delete()
    return redirect("home")


@login_required(login_url=LOGIN_URL)
def edit_employee(request, employee_id):
    specific_employee = EmployeeBaseInformation.objects.get(pk=employee_id)
    form = EmployeeBaseInformationForm(request.POST or None, instance=specific_employee)
    if form.is_valid():

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(
                EmployeeBaseInformation
            ).pk,
            object_id=specific_employee.id,
            object_repr=f"{specific_employee.first_name} {specific_employee.last_name} working at {specific_employee.place}",
            action_flag=CHANGE,
        )

        form.save()
        return redirect("home")
    return render(
        request,
        "employee_management/form.html",
        {"employee": specific_employee, "form": form},
    )


@login_required(login_url=LOGIN_URL)
def view_employee(request, employee_id):
    specific_employee = EmployeeBaseInformation.objects.get(pk=employee_id)
    days_started_since = (date.today() - specific_employee.start_date).days
    return render(
        request,
        "employee_management/view_employee.html",
        {
            "specific_employee": specific_employee,
            "days_started_since": days_started_since,
        },
    )


@login_required(login_url=LOGIN_URL)
def home_location(request):
    dct_info = {}
    number_employee = len(list(EmployeeBaseInformation.objects.all()))
    number_location = len(list(LocationForWorking.objects.all()))
    filename = DT.now().strftime("%B_%d_%Y") + "_location_backup"

    for location in LocationForWorking.objects.all():
        dct_info[location] = (
            list(EmployeeBaseInformation.objects.filter(place=location)),
            len(list(EmployeeBaseInformation.objects.filter(place=location))),
        )

    return render(
        request,
        "employee_management/location_home.html",
        {
            "dct_info": dct_info,
            "number_employee": number_employee,
            "number_location": number_location,
            "filename": filename
        },
    )


@login_required(login_url=LOGIN_URL)
def submit_location(request):
    form = LocationForWorkingForm()
    if request.method == "POST":
        form = LocationForWorkingForm(request.POST)
        if form.is_valid():
            instance = form.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(
                    LocationForWorking
                ).pk,
                object_id=instance.id,
                object_repr=f"{instance.location_name}",
                action_flag=ADDITION,
            )
            return redirect("home-location")
    return render(request, "employee_management/location_form.html", {"form": form})


@login_required(login_url=LOGIN_URL)
def delete_location(request, location_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(LocationForWorking).pk,
        object_id=specific_location.id,
        object_repr=f"{specific_location.location_name} [Place]",
        action_flag=DELETION,
    )
    location_clone = LocationForWorkingClone(
        location_name=specific_location.location_name,
        notes=specific_location.notes,
        custom_id=specific_location.id,
    )
    location_clone.save()
    specific_location.delete()
    return redirect("home-location")


@login_required(login_url=LOGIN_URL)
def edit_location(request, location_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    form = LocationForWorkingForm(request.POST or None, instance=specific_location)
    if form.is_valid():
        instance = form.save()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(LocationForWorking).pk,
            object_id=specific_location.id,
            object_repr=f"{specific_location.location_name}",
            action_flag=CHANGE,
        )
        return redirect("home-location")
    return render(
        request,
        "employee_management/location_form.html",
        {"specific_location": specific_location, "form": form},
    )


@login_required(login_url=LOGIN_URL)
def view_location(request, location_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    new_dct = {}

    all_weekly_calendar_from_specific_location = (
        WeeklyCalendarFromLocation.objects.filter(location_place=specific_location)
    )

    for weekly_calendar in all_weekly_calendar_from_specific_location:
        lst = []
        for employee in EmployeeBaseInformation.objects.filter(place=specific_location):

            try:
                total_hours = sum(
                    [
                        int(hour)
                        for hour in str(
                            WeeklyHoursForEachEmployeeAndLocation.objects.get(
                                specific_employee_working=employee,
                                specific_weekly_calendar=weekly_calendar,
                            )
                        ).split(":")[-7:]
                    ]
                )
                pay_without_bonus = total_hours * employee.salary
                bonus = employee.bonus if employee.bonus else 0
            except (ObjectDoesNotExist, ValueError):
                total_hours = 0
                pay_without_bonus = 0
                bonus = 0

            lst.append(
                (
                    employee,
                    WeeklyHoursForEachEmployeeAndLocation.objects.filter(
                        specific_employee_working=employee
                    ).filter(specific_weekly_calendar=weekly_calendar),
                    (total_hours, pay_without_bonus, bonus),
                )
            )

        # Add 7 days to weekly_calendar.start_date
        starting_day = weekly_calendar.start_date_week
        ending_day = starting_day + datetime.timedelta(days=6)
        lst_day_with_name = []

        number_to_day_week = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }

        [
            lst_day_with_name.append(
                (
                    starting_day + datetime.timedelta(days=i),
                    number_to_day_week[
                        (starting_day + datetime.timedelta(days=i)).weekday()
                    ],
                )
            )
            for i in range(0, 7)
        ]

        new_dct[weekly_calendar, tuple(lst_day_with_name)] = lst

    return render(
        request,
        "employee_management/location_view.html",
        {"specific_location": specific_location, "new_dct": new_dct, "id": "abcbcbc"},
    )


@login_required(login_url=LOGIN_URL)
def add_calendar(request, location_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    form = WeeklyCalendarFromLocationForm(
        initial={"location_place": specific_location, "start_date_week": date.today()}
    )
    if request.method == "POST":
        form = WeeklyCalendarFromLocationForm(request.POST)
        if form.is_valid():
            instance = form.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(
                    WeeklyCalendarFromLocation
                ).pk,
                object_id=instance.id,
                object_repr=f"{instance.start_date_week} calendar for {instance.location_place}",
                action_flag=ADDITION,
            )

            return redirect("view-location", location_id=location_id)

    return render(
        request,
        "employee_management/calendar_hour_form.html",
        {"specific_location": specific_location, "form": form},
    )


@login_required(login_url=LOGIN_URL)
def delete_calendar(request, location_id, calendar_id):
    specific_calendar = WeeklyCalendarFromLocation.objects.get(pk=calendar_id)
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(
            WeeklyCalendarFromLocation
        ).pk,
        object_id=specific_calendar.id,
        object_repr=f"{specific_calendar.start_date_week} @ {specific_calendar.location_place} [Calendar]",
        action_flag=DELETION,
    )

    specific_calendar_clone = WeeklyCalendarFromLocationClone(
        location_place=specific_calendar.location_place,
        start_date_week=specific_calendar.start_date_week,
        custom_id=specific_calendar.id,
    )

    specific_calendar_clone.save()

    specific_calendar.delete()
    return redirect("view-location", location_id=location_id)


@login_required(login_url=LOGIN_URL)
def edit_hours(request, location_id, calendar_id, employee_id, weekly_calendar_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    specific_weekly_calendar = WeeklyCalendarFromLocation.objects.get(pk=calendar_id)
    specific_employee_working = EmployeeBaseInformation.objects.get(pk=employee_id)
    specific_weekly_calendar_based_on_employee = (
        WeeklyHoursForEachEmployeeAndLocation.objects.get(pk=weekly_calendar_id)
    )

    form = WeeklyHoursForEachEmployeeAndLocationForm(
        request.POST or None, instance=specific_weekly_calendar_based_on_employee
    )

    if form.is_valid():
        instance = form.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(
                WeeklyHoursForEachEmployeeAndLocation
            ).pk,
            object_id=instance.id,
            object_repr=f"{instance.specific_employee_working.first_name} {instance.specific_employee_working.last_name} @ {instance.specific_weekly_calendar.start_date_week}",
            action_flag=CHANGE,
        )

        return redirect("view-location", location_id=location_id)

    return render(
        request,
        "employee_management/weekly_hours_form.html",
        {"specific_location": specific_location, "form": form},
    )


@login_required(login_url=LOGIN_URL)
def add_hours(request, location_id, calendar_id, employee_id):
    specific_location = LocationForWorking.objects.get(pk=location_id)
    specific_weekly_calendar = WeeklyCalendarFromLocation.objects.get(pk=calendar_id)
    specific_employee_working = EmployeeBaseInformation.objects.get(pk=employee_id)
    form = WeeklyHoursForEachEmployeeAndLocationForm(
        initial={
            "specific_weekly_calendar": specific_weekly_calendar,
            "specific_employee_working": specific_employee_working,
        }
    )

    if request.method == "POST":
        form = WeeklyHoursForEachEmployeeAndLocationForm(request.POST)
        if form.is_valid():
            instance = form.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(
                    WeeklyHoursForEachEmployeeAndLocation
                ).pk,
                object_id=instance.id,
                object_repr=f"{instance.specific_employee_working.first_name} {instance.specific_employee_working.last_name} working @ {instance.specific_weekly_calendar.location_place} starting {instance.specific_weekly_calendar.start_date_week}",
                action_flag=ADDITION,
            )

            return redirect("view-location", location_id=location_id)
    return render(
        request,
        "employee_management/weekly_hours_form.html",
        {"specific_location": specific_location, "form": form},
    )


@login_required(login_url=LOGIN_URL)
def view_general_notes(request):
    note_instance = GeneralNotes.objects.get(pk=1)
    lst_elements = []
    [lst_elements.append(i) for i in str(note_instance.notes).split("-") if i != ""]

    last_time_modified = GeneralNotes.objects.get(pk=1).modified_date

    dd = DT.now(pytz.utc) - last_time_modified
    if int(round(dd.total_seconds() / 60, 0)) < 1:
        time_delta = f"{dd.seconds} seconds"
    elif dd.days == 0 and int(round(dd.total_seconds() / 60, 0)) < 60:
        time_delta = f"{(int(round(dd.total_seconds()/60, 0)))} minutes"
    elif int(round(dd.total_seconds() / 60, 0)) > 60 and dd.days < 1:
        time_delta = f"{(int(round(int(round(dd.total_seconds()/60, 0)))/60))} hours"
    elif dd.days >= 1:
        time_delta = f"{dd.days} days"

    return render(
        request,
        "employee_management/view_general_notes.html",
        {
            "time_delta": time_delta,
            "lst_elements": lst_elements,
            "num_elements": len(lst_elements),
        },
    )


@login_required(login_url=LOGIN_URL)
def edit_general_notes(request):
    note_instance = GeneralNotes.objects.get(pk=1)

    last_time_modified = GeneralNotes.objects.get(pk=1).modified_date
    form = GeneralNotesForm(request.POST or None, instance=note_instance)
    if form.is_valid():
        instance = form.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(GeneralNotes).pk,
            object_id=instance.id,
            object_repr=f"General notes",
            action_flag=CHANGE,
        )

        return redirect("view-general-notes")
    return render(
        request,
        "employee_management/general_notes_form.html",
        {"note_instance": note_instance, "form": form},
    )


def split(lst, n):
    k, m = divmod(len(lst), n)
    return (lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


@login_required(login_url=LOGIN_URL)
def weekly_calendar_to_pdf(request, calendar_id):
    buff = io.BytesIO()
    c = canvas.Canvas(buff, pagesize=letter, bottomup=0)

    specific_calendar = WeeklyHoursForEachEmployeeAndLocation.objects.filter(
        specific_weekly_calendar=calendar_id
    )

    lines = []

    for specific_calendar in split(
        specific_calendar, math.ceil(len(list(specific_calendar)) / 5)
    ):
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 12)

        for employee in list(specific_calendar):
            lines.append(
                f"From: {employee.specific_weekly_calendar.start_date_week}                 TO: {employee.specific_weekly_calendar.start_date_week + datetime.timedelta(days=7)}"
            )
            lines.append(
                f"{employee.specific_employee_working.first_name} {employee.specific_employee_working.last_name} salary of {employee.specific_employee_working.salary}$/h and bonus of {employee.specific_employee_working.bonus}$ per week"
            )
            lines.append(f'Monday => {(str(employee).split(":")[-7])}')
            lines.append(f'Tuesday => {(str(employee).split(":")[-6])}')
            lines.append(f'Wednesday => {(str(employee).split(":")[-5])}')
            lines.append(f'Thursday => {(str(employee).split(":")[-4])}')
            lines.append(f'Friday => {(str(employee).split(":")[-3])}')
            lines.append(f'Saturday => {(str(employee).split(":")[-2])}')
            lines.append(f'Sunday => {(str(employee).split(":")[-1])}')
            lines.append("=================================")

        [textob.textLine(str(line)) for line in lines]

        c.drawText(textob)
        c.showPage()

    c.save()
    buff.seek(0)

    try:
        name = f"{specific_calendar[0].specific_weekly_calendar.start_date_week}_work_sheet.pdf"
    except IndexError:
        name = "No_file.pdf"

    return FileResponse(buff, as_attachment=True, filename=str(name))


@login_required(login_url=LOGIN_URL)
def view_logs(request):

    logs = list(LogEntry.objects.all().order_by("-action_time"))[:20]
    log_count = len(list(logs))

    return render(
        request,
        "employee_management/view_logs.html",
        {"logs": logs, "log_count": log_count},
    )


@login_required(login_url=LOGIN_URL)
def save_employee(request):
    general_notes = GeneralNotes.objects.get(pk=1)
    all_locations = LocationForWorking.objects.all()
    all_employees = EmployeeBaseInformation.objects.all()
    all_weekly_hours_for_each_employee_and_location = (
        WeeklyHoursForEachEmployeeAndLocation.objects.all()
    )

    buff = io.BytesIO()
    c = canvas.Canvas(buff, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)

    lines = []

    lines.append(f"General notes {general_notes.notes}")

    lines.append(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    for i in all_employees:
        lines.append(
            f"{i.first_name} {i.last_name} working at {i.place} ==== {i.phone_number}"
        )
        lines.append(
            f"starting on {i.start_date} with a salary of {i.salary}/hour and bonus of {i.bonus}/week =====> is a driver? {i.is_driver}"
        )
        lines.append(f"with the following notes: {i.notes}")

        lines.append(f"\n\n\n\n\n\n\n\n\n")

    for line in lines:
        textob.textLine(str(line))

    c.drawText(textob)
    c.showPage()
    c.save()
    buff.seek(0)

    try:
        name = f"employee_backup_{DT.now().day}{DT.now().month}/{DT.now().hour}/{DT.now().minute}.pdf"
    except IndexError:
        name = "error.pdf"

    return FileResponse(buff, as_attachment=True, filename=str(name))


@login_required(login_url=LOGIN_URL)
def save_location(request):
    all_locations = LocationForWorking.objects.all()

    buff = io.BytesIO()
    c = canvas.Canvas(buff, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)

    lines = []

    for i in all_locations:
        lines.append(f"Location: {i.location_name} with the following notes: {i.notes}")

    for line in lines:
        textob.textLine(str(line))

    c.drawText(textob)
    c.showPage()
    c.save()
    buff.seek(0)

    try:
        name = f"location_backup_{DT.now().day}{DT.now().month}/{DT.now().hour}/{DT.now().minute}.pdf"
    except IndexError:
        name = "error.pdf"

    return FileResponse(buff, as_attachment=True, filename=str(name))


@login_required(login_url=LOGIN_URL)
def undo_action(request, specific_id, string_object):
    if string_object.strip().endswith("[place]"):
        clone_instance = LocationForWorkingClone.objects.get(custom_id=specific_id)
        assert_new_location = LocationForWorking(
            location_name=clone_instance.location_name, notes=clone_instance.notes
        )
        return redirect("home-location")
        assert_new_location.save()
    if string_object.strip().endswith("[Employee]"):
        clone_instance = EmployeeBaseInformationClone.objects.get(custom_id=specific_id)
        assert_new_employee = EmployeeBaseInformation(
            first_name=clone_instance.first_name,
            last_name=clone_instance.last_name,
            place=clone_instance.place,
            phone_number=clone_instance.phone_number,
            start_date=clone_instance.start_date,
            salary=clone_instance.salary,
            bonus=clone_instance.bonus,
            is_driver=clone_instance.is_driver,
            notes=clone_instance.notes,
        )
        assert_new_employee.save()
        return redirect("home")

    if string_object.strip().endswith("[Calendar]"):
        clone_instance = WeeklyCalendarFromLocationClone.objects.get(
            custom_id=specific_id
        )
        assert_new_calendar = WeeklyCalendarFromLocation(
            location_place=clone_instance.location_place,
            start_date_week=clone_instance.start_date_week,
        )
        assert_new_calendar.save()
        return redirect("view-location")

    return redirect("home-location")


def changelog(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "CHANGELOG.md")

    string_text = open(file_path, "r")
    new_string = string_text.read()
    html = markdown.markdown(new_string)
    return render(request, "employee_management/changelog.html", {"html": html})
