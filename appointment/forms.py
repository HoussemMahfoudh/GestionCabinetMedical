from django import forms
from appointment.models import Appointment, TimeSlots, Disponibilty
from bootstrap_datepicker_plus import DatePickerInput

class DateInput(forms.DateInput):
    input_type = 'date'

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        disabledates = ['04/24/2020','04/23/2020','04/22/2020']
        fields = ('event_date','time','service') #Les champs a afficher dans la formulaire
        widgets = {
            'event_date': DatePickerInput(
                options={
                    "format": "MM/DD/YYYY",
                    'daysOfWeekDisabled':[0,6],
                    "disabledDates":disabledates,
                    
                },
                attrs={'class':'form-control',
                'type':'text',
                'placeholder': 'Choose a reservation date',}
            ),
        }
        
        localized_fields = '__all__'

    #start = forms.ModelChoiceField(queryset=TimeSlots.objects.all(), required=True)
    #event = forms.DateField(widget = DateInput())