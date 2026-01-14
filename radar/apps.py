import os
import threading
import time

from django.apps import AppConfig


class RadarConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "radar"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        from radar.tasks import send_notifications

        def worker():
            while True:
                print("Start Notifications")
                send_notifications()
                print("End Notifications")
                time.sleep(60 * 60)  # 1 час

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
