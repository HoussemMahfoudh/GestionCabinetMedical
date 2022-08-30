from django.shortcuts import render
from Article.models import Article
from Service.models import Service

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView 
from appointment.models import Appointment, TimeSlots, Event
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

# Create your views here.
def indexView(request):
    articles = Article.objects.all().order_by('-date')[:6]
    services = Service.objects.all()

    context = {
        'articles_instances' : articles,
        'services': services,
    }
    return render(request, 'index.html', context=context)

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
