from django.urls import path
from reservation import views

app_name = 'reservation'

urlpatterns = [
    path('', views.ReservationView.as_view() , name='Reservation'),
    path('list/', views.ReservationListView.as_view() , name='Reservation-list'),
    #path('list/<id>/', views.detail_View , name='Reservation-list'),
    path ('edit/<int:pk>/',views.ReservationUpdateView.as_view(),name='reservation-update'),
    path('delete/<int:pk>/',views.ReservationDeleteView.as_view(),name='reservation-delete'),
]