from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Freelancer
from django.contrib.auth.forms import AuthenticationForm

class FreelancerRegistrationForm(UserCreationForm):
    skills = forms.CharField(max_length=255, required=False)
    experience = forms.CharField(max_length=255,required = False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'experience','skills',]


class FreelancerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

          