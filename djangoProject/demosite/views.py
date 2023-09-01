from .models import Product, Buyer, RegisterForm, UserCart, SelectedProduct, Stock, Warehouse
from .forms import RegistrationForm, DjangoRegistrationForm, LoginForm,PasswordResetRequestForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse
from datetime import datetime
from django.db import IntegrityError, transaction
from django.db.models import F, Sum
from django.http import JsonResponse
import logging
import json

# Вью для демонстрационной страницы
def demo_page(request):
    # Получаем все продукты
    products = Product.objects.annotate(remaining_quantity=Sum('stock__quantity')).all()
    success = False
    product_quantities = Stock.objects.values('product').annotate(total_quantity=Sum('quantity'))
    print("product_quantities ", product_quantities)
    remaining_quantities = {item['product']: item['total_quantity'] for item in product_quantities}
    
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
        'success': success,
        'remaining_quantities': remaining_quantities,
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
        form = DjangoRegistrationForm(request.POST)
        if form.is_valid():
            # Check if a user with the same username or email already exists
            username = form.cleaned_data['login']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                form.add_error('login', 'Пользователь с таким логином уже существует.')
                print('логин уже существует')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Пользователь с таким email уже существует.')
                print('email уже существует')
            else:
                # если уникальные имя пользователя и email - продолжаем регу
                registration = RegisterForm(
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

    return render(request, 'demo.html', {'form': form, 'success': success})

# Вью для страницы авторизации
def login_view(request):
    print('Функция login_view вызвана')
    return render(request, 'login.html')

# Защита от неавторизованных пользователей, вью для dashboard
@login_required
def dashboard(request):
    products = Product.objects.annotate(remaining_quantity=Sum('stock__quantity')).all()
    saved_carts = UserCart.objects.filter(user=request.user)
    print('Сохраненные корзины: ', saved_carts)
    return render(request, 'user.html', {'products': products, 'saved_carts': saved_carts})
    
# Функция для добавления товара в корзину
from django.contrib.auth import get_user_model
from .models import Product, Buyer, RegisterForm, SelectedProduct, UserCart
#Добавление товаров в корзину
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

                # Получаем остаток товара из Stock модели
                stock_quantity = Stock.objects.get(product=product).quantity

                # Проверяем, что выбранное количество не превышает остаток
                if product_quantity <= stock_quantity:
                    # Создаем экземпляр SelectedProduct и связываем его с корзиной пользователя
                    selected_product, created = SelectedProduct.objects.get_or_create(
                        user_cart=user_cart,
                        product=product
                    )
                    stock = Stock.objects.get(product=product)
                    stock.quantity -= product_quantity
                    stock.save()
                    selected_product.quantity = product_quantity
                    selected_product.save()

                    # Рассчитываем общую стоимость корзины
                    total_amount += product.price * product_quantity
                else:
                    return JsonResponse({'error': f'Выбранное количество товара {product.name} превышает остаток в наличии.'})

            except (Product.DoesNotExist, Stock.DoesNotExist):
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
            
            # Use a transaction to ensure data consistency
            with transaction.atomic():
                # Restore stock quantities for products in the cart
                for selected_product in user_cart.selectedproduct_set.all():
                    stock = Stock.objects.get(product=selected_product.product)
                    stock.quantity += selected_product.quantity
                    stock.save()
            
            # Удаляем связанные объекты SelectedProduct
            user_cart.selectedproduct_set.all().delete()
            # Удаляем объект UserCart
            user_cart.delete()
            return JsonResponse({'success': True})

    return JsonResponse({'error': 'Неверный метод запроса.'}, status=400)

#восстановление пароля
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            current_site = get_current_site(request)
            subject = 'Reset your password'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = f"{current_site}{reset_link}"

            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
                'domain': current_site.domain,
            })
            
            send_mail(subject, message, 'noreply@example.com', [email])
            return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')
    
    
# TRANSFERS 

def manage_warehouse(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        try:
            product = Product.objects.get(pk=product_id)
            warehouse, created = Warehouse.objects.get_or_create(product=product)
            warehouse.quantity = quantity
            warehouse.save()
            return redirect('success_url')  # редирект на страницу подтверждения
        except Product.DoesNotExist:
            # продукт не найден
            pass

    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse_form.html', {'products': products, 'warehouses': warehouses})
