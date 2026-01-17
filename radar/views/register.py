from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.conf import settings
from ..models import Profile
from ..forms import EmailForm
from ..utils import (check_captcha, get_client_ip)


def register(request: HttpRequest, is_captcha_error: bool = False):

    reg_form = UserCreationForm()
    email_form = EmailForm()
    html = 'registration/register.html'
    context = {
        "reg_form": reg_form,
        "email_form": email_form,
        "captcha_client_key": settings.CAPTCHA_CLIENT_KEY
    }

    if is_captcha_error:
        context["is_captcha_error"] = True

    return render(request, html, context)


@require_POST
def register_create(request: HttpRequest):
    captcha_token = request.POST.get('smart-token', "")
    ip = get_client_ip(request)

    if ip and check_captcha(captcha_token, ip):
        reg_form = UserCreationForm(request.POST)
        email_form = EmailForm(request.POST)

        if reg_form.is_valid() and email_form.is_valid():
            user = reg_form.save()
            Profile.objects.get_or_create(
                user=user, email=email_form.cleaned_data['email'])
            login(request, user)
            return redirect('/profile')
    return register(request, is_captcha_error=True)
