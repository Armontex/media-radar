from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponseServerError, HttpResponseBadRequest
from apps.providers.enums import Source
from apps.providers import TVMazeProvider, ContentProvider
from apps.core.logger import logger

from ..utils import built_titles_context
from ..mappers import title_to_schema_mapper
from ..models import Profile, Title, Subscription


providers: dict[str, ContentProvider] = {
    Source.TVMAZE.value: TVMazeProvider()
}


@login_required
def subscriptions(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)
    subs = Subscription.objects.filter(profile=profile)

    subscribed = set()
    titles = []
    for sub in subs:
        titles.append(sub.title)
        subscribed.add((sub.title.source, sub.title.external_id))

    context = {
        "subs": built_titles_context(
            titles=titles,
            mapper=title_to_schema_mapper,
            subscribed=subscribed,
            is_authenticated=True
        ),
    }
    return render(request, "radar/subscriptions.html", context)


@require_POST
@login_required
def subscriptions_add_title(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)

    source = request.POST.get("source")
    external_id = request.POST.get("external_id")

    if not source or not external_id:
        logger.error(f"Отсутсвуют данные.", extra={
            "source": source,
            "external_id": external_id
        })
        return HttpResponseBadRequest(400)

    provider = providers.get(source)
    if not provider:
        logger.error(f"Неизвестный провайдер.", extra={
            "source": source,
        })
        return HttpResponseServerError()

    schema = provider.get_title(int(external_id))

    title, _ = Title.objects.get_or_create(
        source=schema.source.value,
        external_id=schema.external_id,
        defaults={
            "name": schema.name,
            "descr": schema.descr,
            "cover_url": schema.cover_url,
            "is_active": schema.is_active,
        }
    )

    Subscription.objects.get_or_create(
        profile=profile,
        title=title,
        is_active=title.is_active
    )

    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
@login_required
def subscriptions_delete_title(request: HttpRequest):
    profile = Profile.objects.get(user=request.user)

    source = request.POST.get("source")
    external_id = request.POST.get("external_id")

    if not source or not external_id:
        logger.error(f"Отсутсвуют данные.", extra={
            "source": source,
            "external_id": external_id
        })
        return HttpResponseBadRequest(400)

    title = Title.objects.get(external_id=int(external_id),
                              source=source)

    sub = Subscription.objects.filter(profile=profile, title=title)
    sub.delete()

    if not Subscription.objects.filter(title=title).exists():
        title.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))
