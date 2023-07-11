from django import forms
from .models import RegistrationForm
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



#КУПИТЬ
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = RegistrationForm
        fields = '__all__'
        
        
class DjangoRegistrationForm(UserCreationForm):
    class Meta:
        
        model = User
        fields = ('username', 'password1', 'password2')
        
        
class LoginForm(AuthenticationForm):
    pass
