from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from Materiels.models import Materiel, Categorie
from Article.models import Article
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count

def searchMateriel(request):
        if request.method == 'GET':
            query= request.GET.get('q')
            submitbutton= request.GET.get('submit')
            if query is not None:
                lookups= Q(title__icontains=query ) | Q(description__icontains=query)
                results= Materiel.objects.filter(lookups).distinct()
                articles = Article.objects.all()
                categories = Categorie.objects.all()
                context={
                    'list_materiel': results,
                    'submitbutton': submitbutton,
                    'articles': articles,
                    'categories': categories,
                    }

                return render(request, 'Materiel/MaterielListView.html', context)

            else:
               return render(request, 'Materiel/MaterielListView.html')

        else:
            return render(request, 'Materiel/MaterielListView.html')


class CategorieListView(ListView):
    model = Categorie
    context_object_name = 'Categorie'
    template_name ='Materiels/CategorieListView.html'
    def get_queryset(self):
        return Categorie.objects.all()




class MaterielListView(ListView):
    model=Materiel
    paginate_by = 3
    context_object_name = 'list_materiel'
    template_name = 'Materiel/MaterielListView.html'
    #listeDesArticles = Article.objects.all()
    def get_queryset(self):
        return Materiel.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MaterielListView, self).get_context_data(**kwargs)
        context['categories'] = Categorie.objects.annotate(total=Count('materiel'))
        context['articles'] = Article.objects.all()
        return context


    

class MaterielDetailView(DetailView):
    model = Materiel
    template_name = 'Materiel/MaterielDetailView.html'

    def get_context_data(self, **kwargs):
        context = super(MaterielDetailView, self).get_context_data(**kwargs)
        context['categories'] = Categorie.objects.annotate(total=Count('materiel'))
        context['materiel_related'] = Materiel.objects.filter(categorie=self.object.categorie).exclude(pk__gte=self.object.pk)
        return context






    

    



