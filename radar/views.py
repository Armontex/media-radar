from django.shortcuts import render
from apps.api.tvmaze import TVMazeProvider
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Title, Subscription
from .forms import EmailForm
from .utils import get_titles_context
from apps.api.enums import Source
from apps.api import TVMazeProvider
from typing import Iterable

tvmaze = TVMazeProvider()


def home(request):
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
            profile=request.user.profile if request.user.is_authenticated
            and hasattr(request.user, "profile") else None),
    }

    return render(request, "radar/home.html", context)


@login_required
def profile(request):
    prof = request.user.profile
    context = {
        "profile": prof,
    }
    return render(request, "radar/profile.html", context)


# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        reg_form = UserCreationForm(request.POST)
        email_form = EmailForm(request.POST)
        if reg_form.is_valid() and email_form.is_valid():
            user = reg_form.save()
            Profile.objects.get_or_create(
                user=user, email=email_form.cleaned_data['email'])
            login(request, user)
            return redirect('/profile')
    else:
        reg_form = UserCreationForm()
        email_form = EmailForm()

    context = {'reg_form': reg_form, "email_form": email_form}

    return render(request, 'registration/register.html', context)


def not_found(request):
    return render(request, "radar/not_found.html")


@login_required
def add_title(request):
    prof: Profile = request.user.profile

    if request.method == 'POST':
        data = {
            "source": request.POST.get("source"),
            "external_id": request.POST.get("external_id"),
        }
        match data["source"]:
            case Source.TVMAZE.value:
                title_schema = tvmaze.get_title(data["external_id"])
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
def delete_title(request):
    prof: Profile = request.user.profile
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
def subscriptions(request):
    prof: Profile = request.user.profile
    subs: Iterable[Subscription] = prof.subscriptions.all()  # type: ignore

    titles = []
    for sub in subs:
        titles.append(sub.title)
        
    context = {
        "subs": get_titles_context(titles, profile=prof),
    }
    return render(request, "radar/subscriptions.html", context)
