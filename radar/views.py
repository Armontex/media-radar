import json

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from .models import Profile, Title, Subscription
from .forms import EmailForm
from .utils import (get_titles_context, check_captcha, get_client_ip,
                    verify_telegram_auth)
from .choices import NotifyChannelChoices

from apps.providers.enums import Source
from apps.providers import TVMazeProvider
from apps.core.config import settings

tvmaze = TVMazeProvider()

User = get_user_model()


def home(request: HttpRequest):
    q = (request.GET.get("q") or "").strip()

    search_results = []
    if q:
        provider = TVMazeProvider()
        search_results = provider.get_titles(q)

    context = {
        "q":
        q,
        "result":
        get_titles_context(
            search_results,
            profile=request.user.profile  # type: ignore 
            if request.user.is_authenticated
            and hasattr(request.user, "profile") else None),
    }

    return render(request, "radar/home.html", context)


@login_required
def profile(request: HttpRequest):
    prof = request.user.profile  # type: ignore
    context = {
        "profile": prof,
    }
    return render(request, "radar/profile.html", context)


def register(request: HttpRequest):

    reg_form = UserCreationForm()
    email_form = EmailForm()
    html = 'registration/register.html'
    context = {
        "reg_form": reg_form,
        "email_form": email_form,
        "captcha_client_key": settings.CAPTCHA_CLIENT_KEY
    }

    if request.method == 'POST':
        captcha_token = request.POST.get('smart-token', "")
        ip = get_client_ip(request)

        if check_captcha(captcha_token, ip):  # type: ignore
            reg_form = UserCreationForm(request.POST)
            email_form = EmailForm(request.POST)

            if reg_form.is_valid() and email_form.is_valid():
                user = reg_form.save()
                Profile.objects.get_or_create(
                    user=user, email=email_form.cleaned_data['email'])
                login(request, user)
                return redirect('/profile')
        else:
            context.setdefault("is_captcha_error", True)

    return render(request, html, context)


def not_found(request: HttpRequest):
    return render(request, "radar/not_found.html")


@login_required
def add_title(request: HttpRequest):
    prof: Profile = request.user.profile  # type: ignore

    if request.method == 'POST':
        data = {
            "source": request.POST.get("source"),
            "external_id": request.POST.get("external_id"),
        }
        match data["source"]:
            case Source.TVMAZE.value:
                title_schema = tvmaze.get_title(
                    data["external_id"])  # type: ignore
            case _:
                raise NotImplementedError(
                    f"Неизвестный провайдер: {data['source']}")
        title = Title.objects.get_or_create(
            name=title_schema.name,
            descr=title_schema.descr,
            cover_url=title_schema.cover_url,
            external_id=title_schema.external_id,
            source=title_schema.source.value,
            is_active=title_schema.is_active)
        subscription = Subscription.objects.create(
            profile=prof,
            title=title[0],
        )
        prof.subscriptions.add(subscription)  # type: ignore

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_title(request: HttpRequest):
    prof: Profile = request.user.profile  # type: ignore
    if request.method == 'POST':
        data = {
            "source": request.POST.get("source"),
            "external_id": request.POST.get("external_id"),
        }
        title = Title.objects.get(external_id=data["external_id"],
                                  source=data["source"])
        sub: Subscription
        for sub in prof.subscriptions.all():  # type: ignore
            if sub.title == title:
                sub.delete()

        if len(list(title.subscriptions.all())) == 0:  # type: ignore
            title.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def subscriptions(request: HttpRequest):
    prof: Profile = request.user.profile  # type: ignore
    subs = Subscription.objects.filter(profile=prof)

    titles = []
    for sub in subs:
        titles.append(sub.title)

    context = {
        "subs": get_titles_context(titles, profile=prof),
    }
    return render(request, "radar/subscriptions.html", context)


def telegram_auth(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not verify_telegram_auth(data, settings.BOT_TOKEN.get_secret_value()):
        return JsonResponse({"error": "Invalid Telegram data"}, status=400)

    tg_id = data.get("id")
    username = f"tg_{data.get("username")}" or f"tg_{tg_id}"

    profile = Profile.objects.filter(telegram_id=tg_id).first()
    if profile:
        user = profile.user
    else:
        user = User.objects.create(username=username)
        Profile.objects.create(user=user,
                               telegram_id=tg_id,
                               main_channel=NotifyChannelChoices.TELEGRAM)
    login(request, user)

    return JsonResponse({"status": "ok"})
