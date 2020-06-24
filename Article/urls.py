from django.urls import path
from Article import views

app_name = 'Article'

urlpatterns = [
    path('',views.ArticleListView.as_view() , name='liste-article'),
    path('search/',views.search , name='search-article'),
    path('<slug:slug>/',views.ArticleDetailView.as_view(), name='detail-article'),
    path('categorie/<slug:slug>/', views.CategorieListView.as_view(), name='filter-categorie'),  
]