from django.urls import path
from .import views 


app_name='Service'

urlpatterns = [

    path('', views.ServiceListView.as_view(),name='ListeService'),
    path('search/',views.searchService, name='search'),
    path ('<slug:slug>/',views.ServiceDetailView.as_view(),name='DetailService'),
    
]
