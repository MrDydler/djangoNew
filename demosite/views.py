from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Product
from .models import Buyer
from .forms import DjangoRegistrationForm, LoginForm


def demo_page(request):
    products = Product.objects.all()
    success = False
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')  # Get the product ID from the form data
            product = Product.objects.get(pk=product_id)  # Retrieve the selected product
            buyer = Buyer(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                buyer_message=form.cleaned_data['message'],
                selected_product=product  # Set the selected product
            )
            buyer.save()
            success = True 
            return redirect('/')
            
    else:
        form = RegistrationForm()
    
    context = {
        'products': products,
        'form': form,
        'success': success
    }
    

    
    return render(request, 'demo.html', context)

#Джанго форма реги
def registration_view(request):
    djangoRegistrationForm = DjangoRegistrationForm()
    return render(request, 'registration.html', {'form': djangoRegistrationForm})


#Джанго форма логина
def login_view(request):
    loginForm = LoginForm()
    return render(request, 'login.html', {'form': loginForm})


def form_submit(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the form data
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = LoginForm()
    
    return render(request, 'demo.html', {'form': form})

