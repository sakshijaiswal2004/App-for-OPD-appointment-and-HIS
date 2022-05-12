"""hspmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("add_doctor/", views.addDoctor, name="addDoc"),
    path("all_doctor/", views.allDoctor, name="allDoc"),
    path("all_patient/", views.allPatients, name="allPatient"),
    path("all_appointment/", views.allAppointments, name="allAppointment"),
    path("update_appointment/<int:id>", views.adminUpdateAppointment, name="updateAppointment"),
    path("delete_appointment/<int:id>", views.deleteAppointment, name="deleteAppointment"),
    path("approve_appointment/<int:id>", views.approveAppointment, name="approveAppointment"),
    path("doctor_appointments/", views.doctorAppointments, name="docAppointment"),
    path("doctor_appointment_complete/<int:id>", views.completeAppointment, name="docAptComplete"),
    path("doctor_patients/<int:id>", views.doctorPatients, name="docPatient"),
    path("doctor_profile/<int:id>", views.doctorProfile, name="docProfile"),
    path("appointment/", views.add_appointment, name="appointment"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="hospital/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="hospital/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="hospital/password_reset_complete.html"), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset")
]

