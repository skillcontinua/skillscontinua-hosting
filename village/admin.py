# File path: C:\hosting\skillscontinua_hosting\village\admin.py
from django.contrib import admin
from .models import (
    CommunityPost, MediaStream, ForumTopic, ForumReply,
    SocialChannel, MonetizationOffer,
)


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ("title", "pillar_tag", "started_by", "is_pinned", "created_at")
    list_filter = ("pillar_tag", "is_pinned")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ForumReplyInline]


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "tier_visibility", "is_published", "is_featured", "created_at")
    list_filter = ("category", "tier_visibility", "is_published", "is_featured")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(MediaStream)
class MediaStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "tier_visibility", "is_featured", "created_at")
    list_filter = ("media_type", "tier_visibility", "is_featured")
    search_fields = ("title", "description")


@admin.register(SocialChannel)
class SocialChannelAdmin(admin.ModelAdmin):
    list_display = ("platform", "handle_or_label", "is_active")
    list_filter = ("is_active",)


@admin.register(MonetizationOffer)
class MonetizationOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "tier", "offer_type", "price_display", "is_highlighted", "is_active")
    list_filter = ("tier", "offer_type", "is_highlighted", "is_active")
    search_fields = ("title", "description")