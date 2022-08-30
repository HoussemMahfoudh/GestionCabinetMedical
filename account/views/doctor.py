from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.shortcuts import redirect, render
from django.views.generic import CreateView,UpdateView,TemplateView
from django.views.generic.base import View
from django.contrib.auth.views import LoginView as SignUp
from account.models import MyUser
from rules.contrib.views import PermissionRequiredMixin
from appointment.models import Appointment
from account.forms import UserForm, UserForm_doct
from account.forms import UserForm, UserProfile,UserProfileDoctor
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import Http404
from reservation.models import ReservationMateriel




class UserFormView(View):
    form_class = UserForm_doct
    template_name = 'registration/register_doctor.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process from data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            # cleaned (normalized) data
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            password1 = form.cleaned_data['password1']
            user.is_doctor = True
            specialite = form.cleaned_data['specialite']
            user.set_password(password1)
            user.save()

            # returns user objects if credentials are correct
            user = authenticate(email=email, password=password1)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index')
                     
        return render(request, self.template_name, {'form': form.as_p})


class LoginView(SignUp):
    template_name = 'registration/login.html'

    def connect(self,request):
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        user = authenticate(email=email, password=password1)
        if user is not None and user.is_active:
            if user.is_doctor:
                login(request, user)
                return redirect('index')
        else:
            return redirect('account:register_doctor')


def logout_user(request):
    logout(request)
    print("Not logged in")
    return redirect('account:login_doctor')

class ProfileView(TemplateView):
    #model = MyUser
    template_name = 'registration/profile5.html'
    #permission_required = 'doctor'
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['reservations'] = ReservationMateriel.objects.filter(user =self.request.user)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_doctor != True:
            return redirect('account:profil_user')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

class ProfileUpdate(UpdateView):
    model = MyUser
    #permission_required = 'doctor'
    form_class = UserProfileDoctor
    template_name = 'registration/edit.html'

    def get_object(self, queryset=None):
        if  self.request.user.is_doctor != True:
            return redirect('account:profile_edit')
        else: 
            return self.request.user 
    

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:profile_editDoctor')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
