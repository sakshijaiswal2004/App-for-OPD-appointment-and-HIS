from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Doctor, Appointment
from patient.models import Patient
from .forms import AppointmentForm, DoctorUserForm, CreateUserForm
from django.contrib import messages


# Create your views here.
@login_required()
def home(request):
    if request.user.is_superuser:
        all_appointments = Appointment.objects.all().order_by('-id')
        return render(request, "hospital/adminAllApt.html", {'appointments': all_appointments})
    elif request.user.is_staff and not request.user.is_superuser:
        dr = request.user.id
        drAppointments = Appointment.objects.filter(doctor__user_id=dr).order_by('-id')
        return render(request, "hospital/doctorAppointments.html", {'appointments': drAppointments})
    else:
        messages.success(request, "Not Authorized")
        return redirect('logout')


def allDoctor(request):
    if request.user.is_superuser:
        all_doc = Doctor.objects.all().order_by('-id')
        return render(request, "hospital/adminAllDoctor.html", {'doctors': all_doc})
    else:
        return redirect("logout")


def allPatients(request):
    if request.user.is_superuser:
        all_patients = Patient.objects.all().order_by('-id')
        return render(request, "hospital/adminAllPatient.html", {'patients': all_patients})
    else:
        return redirect("logout")


def allAppointments(request):
    if request.user.is_superuser:
        all_appointments = Appointment.objects.all().order_by('-id')
        return render(request, "hospital/adminAllApt.html", {'appointments': all_appointments})
    else:
        return redirect("logout")


def adminUpdateAppointment(request, id):
    if request.user.is_superuser:
        if request.method == "POST":
            apt = Appointment.objects.get(pk=id)
            form = AppointmentForm(request.POST, instance=apt)
            dr_id = form.data['doctor']
            dr = Doctor.objects.get(pk=dr_id)
            if form.is_valid():
                if dr.availability:
                    form.save()
                    messages.success(request, "Appointment Updated")
                    return redirect("allAppointment")
                else:
                    messages.success(request, "Doctor not Available")
            else:
                messages.success(request, "Appointment already exist please select other time or date")
        else:
            apt = Appointment.objects.get(pk=id)
            form = AppointmentForm(instance=apt)
        return render(request, "hospital/adminAppointmentUpdate.html", {"form": form})
    else:
        return redirect("logout")


@login_required()
def addDoctor(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            dform = DoctorUserForm(request.POST)

            if form.is_valid() and dform.is_valid():
                form.instance.is_staff = True
                user = form.save()
                dr = dform.save(commit=False)
                permission = Permission.objects.get(name='Can view doctor')
                user.user_permissions.add(permission)
                dr.user = user
                dr.save()

                messages.success(request, "Doctor Registered Successfully")
                return redirect("allDoc")
        else:
            form = CreateUserForm()
            dform = DoctorUserForm()
        return render(request, "hospital/adminAddDoctor.html", {"form": form, "dform": dform})
    else:
        return redirect("logout")


def doctorAppointments(request):
    if request.user.is_staff and not request.user.is_superuser:
        dr = request.user.id
        drAppointments = Appointment.objects.filter(doctor__user_id=dr).order_by('-id')
        return render(request, "hospital/doctorAppointments.html", {'appointments': drAppointments})
    else:
        return redirect("logout")


def doctorProfile(request, id):
    if request.user.is_staff and not request.user.is_superuser:
        if request.method == "POST":
            ur = User.objects.get(pk=id)
            dr = Doctor.objects.get(user_id=id)
            form = CreateUserForm(request.POST, instance=ur)
            dform = DoctorUserForm(request.POST, instance=dr)

            if form.is_valid() and dform.is_valid():
                user = form.save()
                doc = dform.save(commit=False)
                doc.user = user
                doc.save()
                return redirect('/')
        else:
            ur = User.objects.get(pk=id)
            dr = Doctor.objects.get(user_id=id)
            form = CreateUserForm(instance=ur)
            dform = DoctorUserForm(instance=dr)
        return render(request, "hospital/doctorProfile.html", {"form": form, "dform": dform})
    else:
        return redirect("logout")


def deleteAppointment(request, id):
    if request.user.is_superuser:
        if request.method == "POST":
            apt = Appointment.objects.get(pk=id)
            apt.delete()
            messages.success(request, "Appointment Deleted")
            return HttpResponseRedirect("/")
    else:
        messages.success(request, "Don't have permission to delete the appointment")


@login_required()
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        dr_id = form.data['doctor']
        dr = Doctor.objects.get(pk=dr_id)
        if form.is_valid():
            if dr.availability:
                my_p = Patient.objects.get(user=request.user)
                form = form.save(commit=False)
                form.patient = my_p
                form.save()

                messages.success(request, "Appointment Added")
                return redirect('pAppointment')
            else:
                messages.success(request, "Doctor not Available")
        else:
            messages.success(request, "Appointment already exist please select other time or date")
    else:
        form = AppointmentForm()
    return render(request, "hospital/addAppointment.html", {"form": form})


def approveAppointment(request, id):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            apt = Appointment.objects.get(pk=id)
            apt.approve = True
            apt.save()
            messages.success(request, "Appointment Approved")
            if request.user.is_superuser:
                return redirect('allAppointment')
            else:
                return redirect('docAppointment')
    else:
        messages.success(request, "Don't have permission to approve the appointment")


def completeAppointment(request, id):
    if request.user.is_staff and not request.user.is_superuser:
        if request.method == "POST":
            apt = Appointment.objects.get(pk=id)
            apt.complete = True
            apt.save()
            messages.success(request, "Appointment Complete")
            return redirect('docAppointment')
    else:
        messages.success(request, "You don't have permission to complete the appointment  ")
        return redirect('docAppointment')


def doctorPatients(request, id):
    patients = []
    if request.user.is_staff and not request.user.is_superuser:
        dr = Doctor.objects.get(user_id=id)
        apts = Appointment.objects.values_list('patient_id', flat=True).filter(doctor_id=dr)
        patientId = set(apts)
        for pt in patientId:
            patients.append(Patient.objects.get(pk=pt))
        return render(request, "hospital/doctorPatients.html", {'patients': patients})
    else:
        return redirect("logout")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "hospital/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            messages.success(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="hospital/password_reset.html",
                  context={"password_reset_form": password_reset_form})
