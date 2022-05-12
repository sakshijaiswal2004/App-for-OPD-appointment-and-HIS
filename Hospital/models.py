from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from django.core.validators import MinLengthValidator
from .fields import MinuteDateTimeField


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    availability = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_Date = MinuteDateTimeField(unique=True)
    approve = models.BooleanField(null=True)
    complete = models.BooleanField(null=True)
    created = models.DateTimeField(auto_now_add=True)
