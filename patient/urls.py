from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="patient/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(template_name="patient/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("patient_login/", views.patientLogin, name="pLogin"),
    path("patient_delete_appointment/<int:id>", views.patientDeleteAppointment, name="pDelete"),
    path("patient_appointments/", views.patientAppointment, name="pAppointment"),
    path("patient_update_appointment/<int:id>", views.patientUpdateAppointment, name="pUpdateAppointment"),
    path("patient_profile/<int:id>", views.patientProfile, name="pProfile"),
]
