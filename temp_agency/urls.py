from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee_management/', include('employee_management.urls')),
    path("contract_management/", include('contract_management.urls')),
    path("", RedirectView.as_view(url='/employee_management/'), name='login-redirect')
]
