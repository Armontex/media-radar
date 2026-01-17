from django.shortcuts import render
from django.http import HttpRequest
from apps.providers import TVMazeProvider
from ..utils import built_titles_context
from ..models import Profile, Subscription


def home(request: HttpRequest):
    q = (request.GET.get("q") or "").strip()

    search_results = []
    if q:
        provider = TVMazeProvider()
        search_results = provider.get_titles(q)
    
    subscribed = set()
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        subs = Subscription.objects.filter(profile=profile)
        for sub in subs:
            subscribed.add((sub.title.source, sub.title.external_id))

    context = {
        "q": q,
        "result": built_titles_context(
            search_results,
            mapper=lambda x: x,
            subscribed=subscribed,
            is_authenticated=request.user.is_authenticated
        )
    }

    return render(request, "radar/home.html", context)
