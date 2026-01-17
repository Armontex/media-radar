from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import EmailForm, NotifyChannelForm
from ..models import Profile


@login_required
def profile(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)
    email_form = EmailForm()
    channel_form = NotifyChannelForm(
        initial={"channel": profile.main_channel})

    return render(request, "radar/profile.html", {
        "profile": profile,
        "email_form": email_form,
        "channel_form": channel_form
    })


@require_POST
@login_required
def profile_email(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)
    email_form = EmailForm(request.POST)
    if email_form.is_valid():
        profile.email = email_form.cleaned_data["email"]
        profile.save()

    return redirect("profile")


@require_POST
@login_required
def profile_channel(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)
    form = NotifyChannelForm(request.POST)
    if form.is_valid():
        profile.main_channel = form.cleaned_data["channel"]
        profile.save()

    return redirect("profile")
