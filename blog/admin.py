from django.contrib import admin
from .models import Post, Subscription, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("created_at", "author", "tags")
    search_fields = ("title", "content", "author__username", "tags__name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    list_filter = ("subscribed_at",)
    search_fields = ("email",)
    date_hierarchy = "subscribed_at"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
