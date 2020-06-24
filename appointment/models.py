from django.db import models
from account.models import MyUser
from Service.models import Service
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import utc
    
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


class Appointment(models.Model):

    class Meta:
        verbose_name = "Rendez-Vou"
        ordering = ['-pk']

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,)
    event_date = models.DateField()
    time = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,)
    available = models.BooleanField(null=True)
    event = models.OneToOneField(Event,on_delete=models.CASCADE,blank=True, null=True,)

    def __str__(self):
        return 'Rendez-vous numero #{0} - {1} {2}'.format(self.pk, self.user.first_name, self.user.last_name)
    
    def get_absolute_url(self):
        return reverse('Appointment:appointment-edit', kwargs={'pk': self.pk})

    def timedifference(self):
        """
        end = timedelta(self.time.start.hour, self.time.start.minute)
        now = timezone.now()
        todayTime = timedelta(now.hour, now.minute)
        """
        now = datetime.now()
        nowTimeDelta = timedelta(now.month, now.day, now.hour)
        appointmentTimeDelta= timedelta(self.event_date.month, self.event_date.day, self.time.start.hour)
        timediff = nowTimeDelta- appointmentTimeDelta

        days = 0
        hours = 0
        if(now.month == self.event_date.month):
            days = now.day - self.event_date.day
            hours = now.hour - self.time.start.hour


        if(days <= 0):
            return 'inférieur = '+str(days)+','+str(hours)
        return ' supérier = '+ str(days)
    
    

class Disponibilty(models.Model):

    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'En congé #{0} - {1}'.format(self.start, self.end)

    def get_start_time(self):
        return self.start
    
    def get_end_time(self):
        return self.end