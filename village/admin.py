# File path: C:\hosting\skillscontinua_hosting\village\admin.py
from django.contrib import admin
from .models import CommunityPost, MediaStream, ForumTopic, ForumReply, SocialChannel, MonetizationOffer


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 1


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'pillar_tag', 'started_by', 'is_pinned', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ForumReplyInline]


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'is_featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(MediaStream)
admin.site.register(SocialChannel)
admin.site.register(MonetizationOffer)