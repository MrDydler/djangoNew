from django import forms
from .models import RegistrationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RegisterForm
from django.contrib.auth.models import User



#КУПИТЬ
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = RegistrationForm
        fields = '__all__'
        
        
class DjangoRegistrationForm(forms.ModelForm):
    class Meta:
        model = RegisterForm
        fields = '__all__'  
     
class LoginForm(AuthenticationForm):
    # class Meta:
    #     model = User
    #     fields = '__all__'
    pass
    
