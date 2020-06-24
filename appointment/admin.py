from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, TimeSlots, Event, Disponibilty

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id','user','service','event_date','time','available',)
    list_filter = ('id','user','service','event_date','available',)
    search_fields = ('id','user','service','event_date',)

class TimeSlotsAdmin(admin.ModelAdmin):
    list_display = ('pk','start','end')
    list_filter = ('start','end')

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','pk','evenement','time',)
    list_filter = ('id','evenement',)
    search_fields = ('id','evenement',)

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(TimeSlots, TimeSlotsAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Disponibilty)