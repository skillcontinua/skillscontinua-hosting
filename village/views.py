# C:\hosting\skillscontinua_hosting\village\views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import (
    CommunityPost, MediaStream, ForumTopic,
    SocialChannel, MonetizationOffer,
)


def village_home(request):
    """The Village landing: latest posts, media, forum topics, social links."""
    posts = CommunityPost.objects.filter(is_published=True)[:6]
    media = MediaStream.objects.all()[:6]
    topics = ForumTopic.objects.all()[:5]
    channels = SocialChannel.objects.filter(is_active=True)
    offers = MonetizationOffer.objects.filter(is_active=True)[:3]
    return render(request, "village/home.html", {
        "posts": posts,
        "media": media,
        "topics": topics,
        "channels": channels,
        "offers": offers,
    })


def post_list(request):
    """Paginated blog / article list."""
    qs = CommunityPost.objects.filter(is_published=True)
    category = request.GET.get("category")
    if category:
        qs = qs.filter(category=category)
    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "village/post_list.html", {
        "page_obj": page,
        "categories": CommunityPost.CATEGORY_CHOICES,
        "active_category": category,
    })


def post_detail(request, slug):
    post = get_object_or_404(CommunityPost, slug=slug, is_published=True)
    related = CommunityPost.objects.filter(
        is_published=True, category=post.category
    ).exclude(pk=post.pk)[:3]
    return render(request, "village/post_detail.html", {
        "post": post,
        "related": related,
    })


def media_list(request):
    """Reels, podcasts, webinars."""
    media_type = request.GET.get("type")
    qs = MediaStream.objects.all()
    if media_type:
        qs = qs.filter(media_type=media_type)
    return render(request, "village/media_list.html", {
        "media": qs,
        "media_types": MediaStream.MEDIA_TYPE_CHOICES,
        "active_type": media_type,
    })


def forum_list(request):
    """List of forum topics."""
    topics = ForumTopic.objects.all()
    return render(request, "village/forum_list.html", {"topics": topics})


def forum_detail(request, slug):
    """A single forum topic with its replies."""
    topic = get_object_or_404(ForumTopic, slug=slug)
    replies = topic.replies.select_related("author")
    return render(request, "village/forum_detail.html", {
        "topic": topic,
        "replies": replies,
    })
