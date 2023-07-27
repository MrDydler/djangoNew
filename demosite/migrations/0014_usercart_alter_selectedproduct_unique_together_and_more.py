# Generated by Django 4.2.2 on 2023-07-26 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demosite', '0013_selectedproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(through='demosite.SelectedProduct', to='demosite.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='selectedproduct',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='selectedproduct',
            name='user_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='demosite.usercart'),
        ),
        migrations.AlterUniqueTogether(
            name='selectedproduct',
            unique_together={('user_cart', 'product')},
        ),
        migrations.RemoveField(
            model_name='selectedproduct',
            name='user',
        ),
    ]
