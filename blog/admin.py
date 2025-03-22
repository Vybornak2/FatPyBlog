from django.contrib import admin
from .models import Post, Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    list_filter = ("subscribed_at",)
    search_fields = ("email",)
    date_hierarchy = "subscribed_at"
