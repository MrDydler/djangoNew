from .models import Product, Buyer, RegisterForm
from .forms import RegistrationForm, DjangoRegistrationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging

def demo_page(request):
    products = Product.objects.all()
    success = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)

            buyer = Buyer(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                buyer_message=form.cleaned_data['message'],
                selected_product=product
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

def form_submit(request):
    print("Form submit вызвана")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("Пользователь авторизован:", user)
                login(request, user)
                return redirect('dashboard')  
            else:
                
                form.add_error(None, "Неправильный пароль или имя пользователя.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def reg_submit(request):
    success = False
    if request.method == 'POST':
        print('RegisterForm ')
        form = DjangoRegistrationForm(request.POST)
        if form.is_valid():
            registration = RegisterForm (
               login=form.cleaned_data['login'], 
               email=form.cleaned_data['email'],
               password=form.cleaned_data['password'],
               confirmPassword=form.cleaned_data['confirmPassword'],
            )
            registration.save()
            print('RegisterForm сохранена')
            
            success = True
            return redirect('/') 
    else:
        form = DjangoRegistrationForm()
        print('RegisterForm else')

    return render(request, 'demo.html', {'form': form})

def login_view(request):
    print('login_view вызвана')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    products = Product.objects.all()
    print(request.user)
    return render(request, 'user.html', {'products': products})

from django.contrib.auth import get_user_model
from .models import Product, Buyer, RegisterForm, SelectedProduct, UserCart
# ... Your existing view functions ...

#@login_required
#@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        print("add_to_cart POST вызван.")
        logging.debug("POST request received.")
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        if product_id:
            # Get or create the user's cart
            user_cart, created = UserCart.objects.get_or_create(user=request.user)

            # Save the selected product to the user's cart
            selected_product, created = SelectedProduct.objects.get_or_create(
                user_cart=user_cart,
                product_id=product_id
            )
            selected_product.quantity += quantity
            selected_product.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid product ID.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
