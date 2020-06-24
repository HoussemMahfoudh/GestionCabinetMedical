from django.urls import path 
from .import views

app_name = 'Materiel'


urlpatterns = [
    path('categorie/', views.CategorieListView.as_view(),name='ListeCategorie'),
    path('', views.MaterielListView.as_view(),name='ListeMateriels'),
    path('search/',views.searchMateriel, name='search'),
    path ('<slug:slug>/',views.MaterielDetailView.as_view(),name='detailMateriels'),
    
]
