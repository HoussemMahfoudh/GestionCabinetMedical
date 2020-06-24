from django.urls import path
from appointment import views

app_name = 'Appointment'

urlpatterns = [
    path('', views.AppointmentView.as_view() , name='appointment'),
    path('edit/<pk>/', views.AppointmentUpdateView.as_view() , name='appointment-edit'),
    path('delete/<pk>/', views.AppointmentDeleteView.as_view(), name='appointment-delete'), 
    path('list/', views.AppointmentListView.as_view() , name='appointment-list'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    
    
]