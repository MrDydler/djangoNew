from django import forms
from .models import RegistrationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate


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
    def get_success_url(self):
        return reverse_lazy('dashboard')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Неправильный пароль или имя пользователя.")
        return cleaned_data
    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email')
    
