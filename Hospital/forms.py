from django.forms import ModelForm, CheckboxInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget
from .models import Doctor, Appointment


dateTimeOptions = {
    'format': 'dd/mm/yyyy HH:ii P',
    'autoclose': True,
    'showMeridian': True,
    'minuteStep': 30,
    'daysOfWeekDisabled': 6,
}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'E-mail'}


class DoctorUserForm(ModelForm):

    class Meta:
        model = Doctor
        fields = ['phone', 'specialization', 'qualification', 'address', 'availability']
        widgets = {
            'availability': CheckboxInput(attrs={'class': 'required avl'}),
        }
        labels = {'availability': 'Available'}


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_Date']
        widgets = {
            'appointment_Date': DateTimeWidget(options=dateTimeOptions, usel10n=True),
        }


