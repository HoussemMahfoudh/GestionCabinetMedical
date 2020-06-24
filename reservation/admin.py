from django.contrib import admin

# Register your models here.
from reservation.models import ReservationMateriel, TimeSlots, Event


class ReservationMaterielAdmin(admin.ModelAdmin):
    list_display = ('user','Materiel','event_date','time','available',)
    list_filter = ('user','Materiel','event_date','available',)
    search_fields = ('user','Materiel','event_date',)

class TimeSlotsAdmin(admin.ModelAdmin):
    list_display = ('pk','start','end')
    list_filter = ('start','end')

class EventAdmin(admin.ModelAdmin):
    list_display = ('pk','evenement','time',)
    list_filter = ('evenement',)
    search_fields = ('evenement',)

admin.site.register(ReservationMateriel, ReservationMaterielAdmin)
admin.site.register(TimeSlots, TimeSlotsAdmin)
admin.site.register(Event, EventAdmin)