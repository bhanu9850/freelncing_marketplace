from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client
from django.contrib.auth.forms import AuthenticationForm
from .models import *
class ClientRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'company_name']



class ClientLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']  

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description','budget','deadline']      
        help_texts = {
            'budget': 'Budget (in rupees)',
            'deadline':'(YYYY-MM-DD)'
        }      


