from django.contrib import admin
from .models import Doctor, Appointment


# Register your models here.
class Doctors(admin.ModelAdmin):
    list_display = ['id', 'phone', 'specialization', 'qualification', 'address']


admin.site.register(Doctor, Doctors)


class Appointments(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_Date']


admin.site.register(Appointment, Appointments)
