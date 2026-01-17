from django.shortcuts import render
from django.http import HttpRequest


def page_not_found(request: HttpRequest, exception):
    return render(request, "radar/404.html", status=404)
