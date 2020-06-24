from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


from . import views
from .views import user, doctor

app_name = 'account'

urlpatterns =[
    path('register/user', user.UserFormView.as_view(), name='register'),
    path('register/doctor', doctor.UserFormView.as_view(), name='register_doctor'),
    path('login/', user.LoginView.as_view(), name='login'),
    path('login/doctor', doctor.LoginView.as_view(), name='login_doctor'),
    path('logout/user', doctor.logout_user, name='logout'),
    #path('login/', doctor.LoginView.as_view(), name='login_doctor'),
    path('logout/doctor', doctor.logout_user, name='logout_doctor'),
    path('profile/user', user.ProfileView.as_view(), name='profil_user'),
    path('profile/doctor', doctor.ProfileView.as_view(), name='profil_doctor'),
    path('profile_edit/', user.ProfileUpdate.as_view(
        template_name='registration/edit.html', success_url="."), name='profile_edit'),
    path('profile_edit/doctor', doctor.ProfileUpdate.as_view(
        template_name='registration/edit.html', success_url="."), name='profile_edit_doctor'),
    path('change-password/', user.change_password, name='change_password'),
    path('change-password/doctor', doctor.change_password, name='change_passwordDoctor'),
    path(' ', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)