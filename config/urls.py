"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
import radar.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/",
         LoginView.as_view(redirect_authenticated_user=True),
         name="login"),
    path("", radar.views.home, name="home"),
    path("profile/", radar.views.profile, name="profile"),
    path("api/profile/email/", radar.views.profile_email, name="api_profile_email"),
    path("api_profile/channel/", radar.views.profile_channel,
         name="api_profile_channel"),
    path("auth/register/", radar.views.register, name="auth_register"),
    path("api/auth/register/", radar.views.register_create,
         name="api_auth_register"),
    path("subscriptions/", radar.views.subscriptions, name="subscriptions"),
    path("api/subscriptions/title/add",
         radar.views.subscriptions_add_title, name="api_subscriptions_title_add"),
    path("api/subscriptions/title/delete",
         radar.views.subscriptions_delete_title, name="api_subscriptions_title_delete"),
    path("api/auth/telegram/", radar.views.telegram_auth, name="api_auth_telegram")
]

handler404 = "radar.views.page_not_found"
