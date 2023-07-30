from django.contrib import admin
from demosite.models import Buyer
from demosite.models import Stock
from demosite.models import Product
from demosite.models import RegisterForm, UserCart, SelectedProduct
from .models import User

# Register your models here.
admin.site.register(Buyer)
admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(RegisterForm)
admin.site.register(UserCart)
admin.site.register(SelectedProduct)