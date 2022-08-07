from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee_management/', include('employee_management.urls')),
    path("contract_management/", include('contract_management.urls')),
    path("", RedirectView.as_view(url='/employee_management/'), name='login-redirect')
]

handler500 = 'employee_management.views.server_error'
handler404 = 'employee_management.views.custom_page_not_found_view'
