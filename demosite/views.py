from django.shortcuts import render, redirect
from .forms import RegistrationForm, DjangoRegistrationForm, LoginForm
from .models import Product, Buyer
from django.contrib.auth import login, authenticate
from .models import RegisterForm

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
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success = True
            return redirect('home')  
        form = LoginForm()

    return render(request, 'demo.html', {'form': form})


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
