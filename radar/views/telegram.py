import json
from django.views.decorators.http import require_POST
from django.contrib.auth import login, get_user_model
from django.http import HttpRequest, JsonResponse
from apps.core.config import settings
from ..models import Profile
from ..utils import verify_telegram_auth
from ..choices import NotifyChannelChoices


@require_POST
def telegram_auth(request: HttpRequest):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not verify_telegram_auth(data, settings.BOT_TOKEN.get_secret_value()):
        return JsonResponse({"error": "Invalid Telegram data"}, status=400)

    tg_id = data.get("id")
    if not tg_id:
        return JsonResponse({"error": "Telegram id is missing"}, status=400)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user = profile.user
        if not profile.telegram_id:
            if Profile.objects.filter(telegram_id=tg_id):
                return JsonResponse(
                    {
                        "status": "error",
                        "code": "telegram_id_already_bound",
                        "detail": "Этот Telegram уже привязан к другому аккаунту.",
                    },
                    status=409,
                )
            profile.telegram_id = tg_id
            profile.save(update_fields=["telegram_id"])
    else:
        profile = Profile.objects.filter(telegram_id=tg_id).first()
        if profile:
            user = profile.user
        else:
            username = f"tg_{data.get('username')}" or f"tg_{tg_id}"
            user = get_user_model().objects.create(username=username)
            Profile.objects.create(
                user=user,
                telegram_id=tg_id,
                main_channel=NotifyChannelChoices.TELEGRAM,
            )

    login(request, user)
    return JsonResponse({"status": "ok"})
