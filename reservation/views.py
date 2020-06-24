
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from reservation.models import ReservationMateriel , TimeSlots, Event
from django import forms
from reservation.forms import ReservationMaterielForm
from Materiels.models import Materiel
import datetime
from django.contrib import messages
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ReservationView(TemplateView):
    form_class = ReservationMaterielForm #Appel la formulaire
    template_name = "reservation/Reservation.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        user = request.user
        if request.user.is_anonymous:
            messages.add_message(request, messages.INFO, 'Vous devez vous connecté pour réserver un matériel.')
            return redirect('account:login')
        form = ReservationMaterielForm(request.POST) #instace du formulaire
        if form.is_valid(): #recupération des champs de la formulaire
            
            validation = True
            Reservation = form.save(commit = False) #before saving data we got work to do
            event_date = form.cleaned_data.get("event_date") #recuperation de la date du formulaire
            time = form.cleaned_data.get("time") #recuperation de temps du formulaire
            events = Event.objects.all() # recupération des evenement de la table event pour vérifcation

            if event_date < datetime.date.today(): #test si la date n'est pas dans le passé
                messages.warning(request, 'La date ne peut etre dans le passé !!')
                validation = False

            if (validation == True): #test si date et temps pris ne sont pas déja pris par un autre utilisateur
                for e in events:
                    if ((e.evenement == event_date) and (e.time == time)):
                        validation = False

            if (validation == True):      
                event = Event.objects.create_event(event_date,time) #si tout est bon creation d'un object event et le sauvegarder dans la base de donnée
                Reservation.user = request.user # prendre l'utilisateur connecté
                Reservation.event = event # link 1 to 1
                Reservation.save() # sauvgarder dans la base DD le rendez vous
                messages.success(request, 'Réservation prise avec succées', extra_tags="success")
            else:
                messages.error(request, 'Date et Heure non disponible')
        return render(request, 'reservation/Reservation.html', {'form': form, 'user':user, 'reservation':Reservation})



class ReservationListView(LoginRequiredMixin,ListView):
    
    model = ReservationMateriel
    template_name = 'reservation/ReservationListView.html'
    context_object_name = 'reservations'

    
    def get_queryset(self):
        user = self.request.user #connected user
        reservationList = ReservationMateriel.objects.filter(user=user) #filter les rendez vous par user
        return reservationList

    def get_context_data(self, **kwargs):
        context = super(ReservationListView, self).get_context_data(**kwargs) 
        context['events'] = Event.objects.all()
        return context



class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = ReservationMateriel
    form_class = ReservationMaterielForm
    template_name = "reservation/ReservationUpdateView.html"
    success_url = reverse_lazy('reservation:reservation-update')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only owner can update appointment """
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404('You Are Not The Owner Of This Reservation')
        return super(ReservationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        reservationid = self.kwargs['pk']
        return reverse_lazy('reservation:reservation-update', kwargs={'pk': reservationid})

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.event_date < datetime.date.today():
            messages.warning(self.request, 'La Date Ne Peut Etre Dans Le Passé.')
            return redirect('reservation:reservation-update', pk=(instance.pk))
        
        #events = Event.objects.all()
        idEvent = instance.event.id
        eventValidation = Event.objects.exclude(id=idEvent)
        for e in eventValidation:  
            if ((e.evenement == instance.event_date) and (e.time == instance.time)):
                messages.warning(self.request, 'Date et Heure Déjà Pris, Veuillez Choisir Une Autre Date Ou Une Autre Heure')
                return redirect('reservation:reservation-update', pk=(instance.pk))

        Event.objects.filter(pk=instance.event.id).delete()
        event = Event.objects.create_event(instance.event_date,instance.time)
        instance.user = self.request.user
        instance.event = event
        instance.save()
        messages.success(self.request, 'Réservation Mise A Jour.')
        return redirect(self.request.path_info)



class ReservationDeleteView(DeleteView):
    model=ReservationMateriel
    success_url=reverse_lazy('reservation:Reservation-list') 

    def get_object(self, queryset=None):
        obj = super(ReservationDeleteView, self).get_object()
        if obj.user != self.request.user:
            raise Http404('You Are Not The Owner Of This Reservation.')
        Event.objects.filter(pk=obj.event.id).delete()
        return obj






