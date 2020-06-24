from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth.views import LoginView as SignUp
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.generic import View
from account.models import MyUser 
from rules.contrib.views import PermissionRequiredMixin
from appointment.models import Appointment
from account.forms import UserForm,UserProfile
from django.urls import reverse_lazy
from django.contrib import messages


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process from data
    def post(self, request):
        form = self.form_class(request.POST)
        users = MyUser.objects.all()
        exist = False
        if form.is_valid():
            
            user = form.save(commit=False)

            for u in users:
                if u.email == form.cleaned_data['email']:
                    messages.error('Email déjà pris. Veuillez saisir un autre email ou se connecter.')
                    exist = True    
            #cleaned (normalized) data
            if exist == False:
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                date_of_birth = form.cleaned_data['date_of_birth']
                phone_number = form.cleaned_data['phone_number']
                address = form.cleaned_data['address']
                password1 = form.cleaned_data['password1']
                user.is_patient = True
                user.set_password(password1)
                user.save()

                # returns user objects if credentials are correct
                user = authenticate(email=email, password=password1)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


class LoginView(SignUp):
    template_name = 'registration/login.html'

    def connect(self,request):
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        user = authenticate(email=email, password=password1)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            return redirect('account:register')


def logout_user(request):
    logout(request)
    print("Not logged in")
    return redirect('account:login')


class ProfileView(TemplateView):
    #model = MyUser
    template_name = 'registration/profile5.html'
    #permission_required = 'patient'
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(user =self.request.user)
        return context
        
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_patient != True:
            return redirect('account:profil_doctor')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class ProfileUpdate(UpdateView):
    model = MyUser
    #permission_required = 'patient'
    form_class = UserProfile
    template_name = 'registration/edit.html'  

    def get_object(self, queryset=None):
        if  self.request.user.is_patient != True:
            return redirect('account:profile_edit_doctor')
        else:
            return self.request.user

    


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:profil_user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })






