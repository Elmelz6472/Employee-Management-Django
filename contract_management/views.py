from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee_management.models import LocationForWorking

URL_LOGIN = '../employee_management/login'

@login_required(login_url=URL_LOGIN)
def home_contract(request):
    all_locations = LocationForWorking.objects.all()
    print(all_locations)
    return render(request, "contract_management/home.html", {"all_locations":all_locations})

