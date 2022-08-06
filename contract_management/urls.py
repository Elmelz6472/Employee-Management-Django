from django.urls import path
from . import views



urlpatterns = [
    path("", views.home_contract, name="home-contract")
]