from .models import Product, Buyer, RegisterForm, UserCart, SelectedProduct
from .forms import RegistrationForm, DjangoRegistrationForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import IntegrityError
from django.db.models import F, Sum
from django.http import JsonResponse
import logging
import json

# Вью для демонстрационной страницы
def demo_page(request):
    # Получаем все продукты
    products = Product.objects.all()
    success = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)

            # Создаем новую запись о покупателе
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

# Вью для отправки формы авторизации
def form_submit(request):
    print("Функция form_submit вызвана")
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

# Вью для отправки формы регистрации
def reg_submit(request):
    success = False
    if request.method == 'POST':
        print('Функция reg_submit: Обработка формы RegisterForm')
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
        print('Функция reg_submit: Форма RegisterForm - else')

    return render(request, 'demo.html', {'form': form})

# Вью для страницы авторизации
def login_view(request):
    print('Функция login_view вызвана')
    return render(request, 'login.html')

# Защита от неавторизованных пользователей, вью для dashboard
@login_required
def dashboard(request):
    products = Product.objects.all()
    saved_carts = UserCart.objects.filter(user=request.user)
    print('Сохраненные корзины: ', saved_carts)
    return render(request, 'user.html', {'products': products, 'saved_carts': saved_carts})

# Функция для добавления товара в корзину
from django.contrib.auth import get_user_model
from .models import Product, Buyer, RegisterForm, SelectedProduct, UserCart

def add_to_cart(request):
    if request.method == 'POST':
        print("Функция add_to_cart вызвана.")
        logging.debug("Получен POST запрос.")
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart_name = request.POST.get('cart_name', 'default')

        if product_id:
            # Получаем или создаем корзину пользователя
            user_cart, created = UserCart.objects.get_or_create(user=request.user)

            # Сохраняем выбранный товар в корзине пользователя
            selected_product, created = SelectedProduct.objects.get_or_create(
                user_cart=user_cart,
                product_id=product_id
            )
            selected_product.quantity += quantity
            selected_product.save()

            # Обновляем название корзины
            user_cart.name = cart_name
            user_cart.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Неверный идентификатор товара.'})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса.'}, status=400)

# Функция сохранения корзины
@login_required
@csrf_exempt
def save_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Получаем данные JSON, отправленные со стороны клиента

        # Получаем или создаем корзину пользователя
        user_cart, created = UserCart.objects.get_or_create(user=request.user)
        user_cart.name = f"Корзина {UserCart.objects.filter(user=request.user).count()}"
        user_cart.save()

        # Сбрасываем продукты в корзине и обновляем выбранные продукты
        user_cart.products.clear()
        total_amount = 0

        # Предполагаем, что данные - это объект с идентификаторами продуктов в качестве ключей и количеством в качестве значений
        for product_id, product_quantity in data.items():
            try:
                # Находим продукт на основе его идентификатора
                product = Product.objects.get(pk=product_id)

                # Создаем экземпляр SelectedProduct и связываем его с корзиной пользователя
                selected_product, created = SelectedProduct.objects.get_or_create(
                    user_cart=user_cart,
                    product=product
                )
                selected_product.quantity = product_quantity
                selected_product.save()

                # Рассчитываем общую стоимость корзины
                total_amount += product.price * product_quantity

            except Product.DoesNotExist:
                # Обрабатываем случай, когда продукт с указанным идентификатором не существует
                pass

        # Обновляем общую стоимость корзины
        user_cart.total_amount = total_amount
        user_cart.save()

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Неверный метод запроса.'}, status=400)

# Функция удаления корзины
@login_required
@csrf_exempt
def delete_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Получаем данные JSON, отправленные со стороны клиента
        cart_id = data.get('cart_id')

        if cart_id:
            user_cart = get_object_or_404(UserCart, id=cart_id, user=request.user)
            # Удаляем связанные объекты SelectedProduct
            user_cart.selectedproduct_set.all().delete()
            # Удаляем объект UserCart
            user_cart.delete()
            return JsonResponse({'success': True})

    return JsonResponse({'error': 'Неверный метод запроса.'}, status=400)
