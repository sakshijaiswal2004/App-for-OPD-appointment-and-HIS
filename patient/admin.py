from django.contrib import admin
from .models import *


# Register your models here.

class Patients(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender', 'phone', 'address']


admin.site.register(Patient, Patients)


class Genders(admin.ModelAdmin):
    list_display = ['id', 'gender']


admin.site.register(Gender, Genders)
