"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from django.urls import path, include
from radar.views import (home, profile, register, add_title,
                         delete_title, subscriptions, telegram_auth, set_channel)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("profile/", profile, name="profile"),
    path("profile/channel/", set_channel, name="profile_channel"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/',
         LoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('auth/register/', register, name='register'),
    path('subscriptions/add/', add_title, name='subscriptions_add'),
    path('subscriptions/delete/', delete_title, name='subscriptions_delete'),
    path('auth/telegram/', telegram_auth, name='telegram_auth')
]

handler404 = "radar.views.page_not_found"