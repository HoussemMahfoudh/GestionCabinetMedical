from django.db import models
from Materiels.models import Materiel 
from account.models import MyUser
from ppemedical.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse

# Create your models here.
class TimeSlots(models.Model):
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return '%s' % (self.start.strftime("%I:%M"))

    def __unicode__(self):
        return u'%s - %s' % (self.start, self.end)
    
class EventManager(models.Manager):
    
    def create_event(self, evenement, temps):
        event = self.create(evenement=evenement,time=temps)
        return event


class Event(models.Model):
    
    objects = EventManager()
    evenement = models.DateField()
    time = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,)

    def __str__(self):
        return 'Event #{0} - {1}'.format(self.pk, self.evenement)
    

class ReservationMateriel(models.Model):
    class Meta:
        ordering = ['-pk']

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,)
    Materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE,)
    event_date = models.DateField()
    time = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,)
    available = models.BooleanField(null=True)
    event = models.OneToOneField(Event,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return 'Reservation numero #{0} - {1} {2}'.format(self.pk, self.user.first_name, self.user.last_name)
    

    def get_absolute_url(self):
        return reverse('reservation:reservation-update', kwargs={'pk': self.pk})