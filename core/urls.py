"""
URL configuration for sandooq project.

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
from django.urls import path

from finance.views import mark_installments_as_paid
from users.views import user_dashboard, user_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='front/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('mark-installments-as-paid/', mark_installments_as_paid, name='mark_installments_as_paid'),
]
