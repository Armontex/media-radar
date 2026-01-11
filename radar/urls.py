from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.profile, name="account"),
    path('accounts/register/', views.register, name='register'),
]