from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RegisterForm

@receiver(post_save, sender=RegisterForm)
def create_user_from_register_form(sender, instance, created, **kwargs):
    if created:
        # Create a new User instance with the data from the RegisterForm instance
        user = User.objects.create_user(username=instance.login, password=instance.password)
        user.is_staff = True
        user.save()