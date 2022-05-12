from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CreateUser, PatientUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Patient
from hospital.models import Appointment, Doctor
from hospital.forms import AppointmentForm


def register(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        pform = PatientUserForm(request.POST)

        if form.is_valid() and pform.is_valid():
            user = form.save()
            std = pform.save(commit=False)
            std.user = user
            std.save()

            messages.success(request, "Patient Registered Successfully")
            return redirect("login")
    else:
        form = CreateUser()
        pform = PatientUserForm()
    return render(request, "patient/register.html", {"form": form, "pform": pform})


def patientLogin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:
                login(request, user)
                return redirect("pAppointment")
            else:
                return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "patient/patientLogin.html", {"form": form})


def patientProfile(request, id):
    if request.method == "POST":
        ur = User.objects.get(pk=id)
        pr = Patient.objects.get(user_id=id)
        form = CreateUser(request.POST, instance=ur)
        pform = PatientUserForm(request.POST, instance=pr)

        if form.is_valid() and pform.is_valid():
            user = form.save()
            per = pform.save(commit=False)
            per.user = user
            per.save()
            return redirect("pLogin")
    else:
        ur = User.objects.get(pk=id)
        pr = Patient.objects.get(user_id=id)
        form = CreateUser(instance=ur)
        pform = PatientUserForm(instance=pr)
    return render(request, "patient/patientProfile.html", {"form": form, "pform": pform})


def patientAppointment(request):
    pr = request.user.id
    apt = Appointment.objects.filter(patient__user_id=pr).order_by('-id')
    return render(request, "patient/patientAppointments.html", {'appointments': apt})


def patientDeleteAppointment(request, id):
    pr = request.user.id
    if request.method == "POST":
        apt = Appointment.objects.get(pk=id)
        apt.delete()
        messages.success(request, "Appointment Deleted")
        apt = Appointment.objects.filter(patient__user_id=pr).order_by('-id')
        return render(request, "patient/patientAppointments.html", {'appointments': apt})


def patientUpdateAppointment(request, id):
    pr = request.user.id
    if request.method == "POST":
        apt = Appointment.objects.get(pk=id)
        form = AppointmentForm(request.POST, instance=apt)
        dr_id = form.data['doctor']
        dr = Doctor.objects.get(pk=dr_id)
        if form.is_valid():
            if dr.availability:
                form.save()
                messages.success(request, "Appointment Updated")
                appointment = Appointment.objects.filter(patient__user_id=pr).order_by('-id')
                return render(request, "patient/patientAppointments.html", {'appointments': appointment})
            else:
                messages.success(request, "Doctor not Available")
        else:
            messages.success(request, "Appointment already exist please select other time or date")
    else:
        apt = Appointment.objects.get(pk=id)
        form = AppointmentForm(instance=apt)
    return render(request, "hospital/adminAppointmentUpdate.html", {"form": form})
