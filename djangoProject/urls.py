"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from demosite import views
from demosite.views import demo_page
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from demosite.views import login_view
from django.urls import reverse_lazy



urlpatterns = [
    path('', views.demo_page, name='demo'),
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    #loginForm
    path('form_submit/', views.form_submit, name='form_submit'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reg_submit/',views.reg_submit, name='reg_submit'),
    path('user/', views.dashboard, name='user'),
    #корзина
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    #восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #перенос склад-прод
    path('manage_warehouse/', views.manage_warehouse, name='manage_warehouse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from demosite.apps import DemositeConfig
# DemositeConfig.ready()