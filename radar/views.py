from django.shortcuts import render
from apps.api.tvmaze import TVMazeProvider

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

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

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
