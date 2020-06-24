from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView 
from appointment.models import Appointment, TimeSlots, Event
from Service.models import Service
from account.models import MyUser
from appointment.forms import AppointmentForm
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
import datetime as dd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404
from django.http import HttpResponse
from datetime import datetime
from django.utils.safestring import mark_safe
from .utils import Calendar



class AppointmentView(TemplateView):
    form_class = AppointmentForm #Appel la formulaire
    template_name = "appointment/appointment.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    
    def post(self, request):
        user = request.user
        if request.user.is_anonymous:
            messages.add_message(request, messages.INFO, 'Vous devez vous connecté pour prendre un rendez-vous.')
            return redirect('account:login')
        form = AppointmentForm(request.POST)

        if form.is_valid():
            validation = True
            rendezVous = form.save(commit = False)
            event_date = form.cleaned_data.get("event_date")
            time = form.cleaned_data.get("time")
            events = Event.objects.all() #recupération des rendez-vous en cours

            if event_date < dd.date.today():
                messages.warning(request, 'La date ne peut etre dans le passé.')
                validation = False

            if (validation == True): #test si date et temps pris ne sont pas déja pris par un autre utilisateur
                for e in events:
                    if ((e.evenement == event_date) and (e.time == time)):
                        validation = False

            if (validation == True):      
                event = Event.objects.create_event(event_date,time)
                rendezVous.user = request.user
                rendezVous.event = event
                rendezVous.save()
                messages.success(request, 'Rendez-Vous Pris.', extra_tags="success")
            else:
                messages.error(request, 'Date et Heure non disponible')
        return render(request, 'appointment/appointment.html', {'form': form, 'user':user, 'appointment':rendezVous})


class AppointmentListView(LoginRequiredMixin,ListView):

    model = Appointment
    template_name = 'appointment/AppointmentListView.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        appointmentList = Appointment.objects.filter(user=user)
        return appointmentList

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs) 
        context['events'] = Event.objects.all()
        context['dateToday'] = dd.date.today()
        context['timeNow'] = timezone.now()
        return context


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):

    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/AppointmentUpdate.html'
    success_url = reverse_lazy('Appointment:appointment-edit')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only owner can update appointment """
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404('You Are Not The Owner Of This Appointment')
        return super(AppointmentUpdateView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.event_date < dd.date.today():
            messages.warning(self.request, 'La Date Ne Peut Etre Dans Le Passé.')
            return redirect('Appointment:appointment-edit', pk=(instance.pk))
        
        #events = Event.objects.all()
        idEvent = instance.event.id
        eventValidation = Event.objects.exclude(id=idEvent)
        for e in eventValidation:  
            if ((e.evenement == instance.event_date) and (e.time == instance.time)):
                messages.warning(self.request, 'Date et Heure Déjà Pris, Veuillez Choisir Une Autre Date Ou Une Autre Heure')
                return redirect('Appointment:appointment-edit', pk=(instance.pk))

        Event.objects.filter(pk=instance.event.id).delete()
        event = Event.objects.create_event(instance.event_date,instance.time)
        instance.user = self.request.user
        instance.event = event
        instance.save()
        messages.success(self.request, 'Rendez-Vous Mise A Jour.')
        return redirect(self.request.path_info)

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):

    model = Appointment
    success_url = reverse_lazy('Appointment:appointment-list')


    def get_object(self, queryset=None):
        obj = super(AppointmentDeleteView, self).get_object()
        if obj.user != self.request.user:
            raise Http404('You Are Not The Owner Of This Appointment.')
        Event.objects.filter(pk=obj.event.id).delete()
        return obj
            
                
def calendar(request):
    return HttpResponse('hello')

class CalendarView(ListView):
    model = Appointment
    template_name = 'appointment/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()