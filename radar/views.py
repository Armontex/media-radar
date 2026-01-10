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