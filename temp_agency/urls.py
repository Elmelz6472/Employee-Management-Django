from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee_management/', include('employee_management.urls')),
    path("contract_management/", include('contract_management.urls'))
]
