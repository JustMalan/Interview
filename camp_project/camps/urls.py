from django.urls import path
from . import views

app_name = "camps"

urlpatterns = [
    path("", views.home, name="home"),
    path("camps/", views.camp_list, name="camp_list"),
    path("camps/new/", views.camp_create, name="camp_create"),
    path("registrations/", views.registration_list, name="registration_list"),
    path("registrations/new/", views.registration_create, name="registration_create"),
    path(
        "registrations/<int:pk>/", views.registration_detail, name="registration_detail"
    ),
    path(
        "registrations/<int:pk>/student/new/",
        views.registration_add_student,
        name="registration_add_student",
    ),
    path(
        "registrations/<int:pk>/camp/add/",
        views.registration_add_camp,
        name="registration_add_camp",
    ),
]
