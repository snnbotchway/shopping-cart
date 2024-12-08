from django.urls import path

from . import views

urlpatterns = [
    path("healthcheck/", views.health_check, name="health_check"),
]
