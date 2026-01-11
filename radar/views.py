from django.shortcuts import render
from apps.api.tvmaze import TVMazeProvider
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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


def profile(request):
    return render(request, "radar/profile.html")


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def not_found(request):
    return render(request, "radar/not_found.html")