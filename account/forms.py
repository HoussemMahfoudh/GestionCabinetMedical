from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.db import transaction
from .models import MyUser
from django.contrib.auth.forms import PasswordChangeForm


class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    # first_name = forms.CharField(label="First Name",widget=forms.TextInput)
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'city', 'address']
        
        widgets = {
            'date_of_birth': DateInput(),
        }

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your name here',
            }
        )
    )




    phone_number = forms.DecimalField(
        max_digits = 8,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'number with 8 digits',
                'pattern' : '[234579]{1}[0-9]{7}',
            }
        )
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")


        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # save the provided in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserForm_doct(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    #password = forms.CharField(widget=forms.PasswordInput)

    # first_name = forms.CharField(label="First Name",widget=forms.TextInput)
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'date_of_birth', 'gender', 'city', 'address','specialite']

        widgets = {
            'date_of_birth': DateInput(),
        }

    phone_number = forms.DecimalField(
        max_digits=8,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'number with 8 digits',
            }
        )
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # save the provided in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'date_of_birth','phone_number','gender', 'city', 'address', 'is_active', 'is_admin', 'is_doctor')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfile(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'date_of_birth', 'gender', 'city', 'address','picture']



