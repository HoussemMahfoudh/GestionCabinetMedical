from django import forms
from reservation.models import ReservationMateriel, TimeSlots
from bootstrap_datepicker_plus import DatePickerInput



class DateInput(forms.DateInput):
    input_type = 'date'


class ReservationMaterielForm(forms.ModelForm):

    class Meta:
        model = ReservationMateriel
        #disabledates = ['04/24/2020','04/23/2020','04/22/2020']
        fields = ('event_date','time','Materiel') #Les champs a afficher dans la formulaire
        widgets = {
            'event_date': DatePickerInput(
                options={
                    "format": "MM/DD/YYYY",
                    'daysOfWeekDisabled':[0,6],
                    #"disabledDates":disabledates,
                }
            ),
        }
        
        localized_fields = '__all__'

    #start = forms.ModelChoiceField(queryset=TimeSlots.objects.all(), required=True)
    #event = forms.DateField(widget = DateInput())