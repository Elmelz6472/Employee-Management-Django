from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("submit", views.submit, name="submit"),
    path(
        "delete_employee/<employee_id>", views.delete_employee, name="delete-employee"
    ),
    path("edit_employee/<employee_id>", views.edit_employee, name="edit-employee"),
    path("view_employee/<employee_id>", views.view_employee, name="view-employee"),
    path("locations", views.home_location, name="home-location"),
    path("locations/submit", views.submit_location, name="submit-location"),
    path(
        "locations/delete_employee/<location_id>",
        views.delete_location,
        name="delete-location",
    ),
    path(
        "locations/edit_employee/<location_id>",
        views.edit_location,
        name="edit-location",
    ),
    path(
        "locations/view_location/<location_id>",
        views.view_location,
        name="view-location",
    ),
    path(
        "locations/add_calendar/<location_id>", views.add_calendar, name="add-calendar"
    ),
    path(
        "locations/view_location/<location_id>/<calendar_id>/<employee_id>",
        views.add_hours,
        name="add-hours",
    ),
    path(
        "locations/view_location/<location_id>/<calendar_id>",
        views.delete_calendar,
        name="delete-calendar",
    ),
    path(
        "locations/view_location/edit_hours/<location_id>/<calendar_id>/<employee_id>/<weekly_calendar_id>",
        views.edit_hours,
        name="edit-hours",
    ),
    path("view_general_notes", views.view_general_notes, name="view-general-notes"),
    path("edit_general_notes", views.edit_general_notes, name="edit-general-notes"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path(
        "weekly_calendar_to_pdf/<calendar_id>",
        views.weekly_calendar_to_pdf,
        name="weekly-calendar-to-pdf",
    ),
    path("view_logs", views.view_logs, name="view-logs"),
    path("save_employee", views.save_employee, name="save-employee"),
    path("save_location", views.save_location, name="save-location"),
    path(
        "undo_action/<specific_id>/<string_object>",
        views.undo_action,
        name="undo-action",
    ),
]
