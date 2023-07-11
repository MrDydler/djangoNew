from django.db import models

class Buyer(models.Model):
    name = models.CharField(max_length=25, blank=False)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=25, blank=False)
    buyer_message = models.TextField(blank=True, max_length=255)
    selected_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    

class RegistrationForm(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        unique_together = ('email',)
        
class User(models.Model):
    username = models.TextField(max_length=25)
    password1 = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    

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
    price = models.FloatField()
    description = models.TextField(max_length=700)
    material = models.CharField(max_length=1, choices=MATERIAL_CHOICES, blank=True)
    image = models.ImageField(upload_to='media/products/')



class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"


    # def __str__(self):
    #     return self.name
