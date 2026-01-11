from django.contrib import admin
from .models import Title, Release, Profile, Subscription, NotificationLog

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'is_active', 'created_at']
    list_filter = ['source', 'is_active']
    search_fields = ['name']

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'season', 'number', 'released_at']
    list_filter = ['title']

@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'telegram_id', 'main_channel', 'register_at']
    list_filter = ['main_channel']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'is_active']
    list_filter = ['is_active']

admin.site.register(NotificationLog)
