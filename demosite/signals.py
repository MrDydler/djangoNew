from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import RegisterForm

@receiver(post_save, sender=RegisterForm)
def create_user_from_register_form(sender, instance, created, **kwargs):
    if created:
        # создаем нового пользователя при запонении регистрационной формы
        user = User.objects.create_user(username=instance.login, password=instance.password, email=instance.email)
        user.is_staff = False
        
        user.save()
        default_group = Group.objects.get(name='authUsers')
        user.groups.add(default_group)