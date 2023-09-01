from django.db import models
from django.contrib.auth.models import User


#когда купил
class Buyer(models.Model):
    name = models.CharField(max_length=25, blank=False)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=25, blank=False)
    buyer_message = models.TextField(blank=True, max_length=255)
    selected_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name} - {self.selected_product.name} ({self.quantity})"


#кнопка купить
class RegistrationForm(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        unique_together = ('email',)
    
#Регистрация 
class RegisterForm(models.Model):
    login = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    password = models.CharField(max_length=25)
    confirmPassword = models.CharField(max_length=25)
    
# product
class Product(models.Model):
    MATERIAL_CHOICES = [
        ("1", "золотой"),
        ("2", "Серебряный"),
        ("3", "Жемчуг"),
        ("4", "Платина"),
        ("5", "Алмаз"),
        ("6", "Медь")
    ]
    name = models.CharField(max_length=255, blank=True)
    id = models.IntegerField(primary_key=True)
    price = models.IntegerField()
    description = models.TextField(max_length=700)
    material = models.CharField(max_length=1, choices=MATERIAL_CHOICES, blank=True)
    image = models.ImageField(upload_to='media/products/')
    
    def __str__(self):
        return f"Продукт {self.name}, ID {self.id}"

#корзина
class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='SelectedProduct')
    name = models.CharField(max_length=100, default='Корзина')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"Карточка пользователя {self.user}"
#остаток товара
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} в остатке"


#соранение корзины
class SelectedProduct(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_cart', 'product',)
        
    def __str__(self):
        return f"Товары {self.user_cart.user}"

#Авторизация
class User(models.Model):
    username = models.TextField(max_length=25)
    password = models.CharField(max_length=25)

#Модель переноса   
class Warehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_stock()

    def update_stock(self):
        stock, _ = Stock.objects.get_or_create(product=self.product)
        print('self.quantity ', self.quantity)
        print('stock.quantity ', stock.quantity)
        stock.quantity = stock.quantity - self.quantity
        stock.save()
    def __str__(self):
        return f"{self.product.name} на складе {self.quantity} шт"