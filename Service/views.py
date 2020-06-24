from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from Service.models import Service
from django.db.models import Q
from django.core.paginator import Paginator




# Create your views here.


def searchService(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query)

            results= Service.objects.filter(lookups).distinct()

            context={'List_Service': results,
                     'submitbutton': submitbutton}

            return render(request, 'Service/ServiceListView.html', context)

        else:
            return render(request, 'Service/ServiceListView.html')

    else:
        return render(request, 'Service/ServiceListView.html')


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'Service/ServiceDetailView.html'


class ServiceListView (ListView):

    model = Service
    context_object_name = 'List_Service'
    template_name = 'Service/ServiceListView.html' 

    def get_queryset(self):
        return Service.objects.all()




    
    
    

