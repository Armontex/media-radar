from django.shortcuts import render
from apps.api.tvmaze import TVMazeProvider
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import EmailForm

def home(request):
    q = (request.GET.get("q") or "").strip()

    search_results = []
    if q:
        provider = TVMazeProvider()
        search_results = provider.get_titles(q)

    context = {
        "q": q,
        "search_results": search_results,
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
                user=user,
                email=email_form.cleaned_data['email']
            )
            login(request, user)
            return redirect('/profile')
    else:
        reg_form = UserCreationForm()
        email_form = EmailForm()

    context = {
        'reg_form': reg_form,
        "email_form": email_form
    }

    return render(request, 'registration/register.html', context)

def not_found(request):
    return render(request, "radar/not_found.html")