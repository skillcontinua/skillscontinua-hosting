# File path: C:\hosting\skillscontinua_hosting\village\views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ForumReplyForm
from .models import (
    CommunityPost, MediaStream, ForumTopic,
    SocialChannel, MonetizationOffer,
)


def village_home(request):
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
    topics = ForumTopic.objects.all()
    return render(request, "village/forum_list.html", {"topics": topics})


def forum_detail(request, slug):
    """Topic view + reply form (login required to post)."""
    topic = get_object_or_404(ForumTopic, slug=slug)
    replies = topic.replies.select_related("author")
    form = ForumReplyForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            # Preserve the intent — send them to login, then back here.
            return redirect(f"/accounts/login/?next={request.path}")

        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            # Auto-badge mentor replies (option (a) + mentor flag).
            reply.is_verified_mentor_answer = bool(
                getattr(request.user, "is_mentor", False)
            )
            reply.save()
            messages.success(request, "Your reply was posted.")
            return redirect("village:forum_detail", slug=topic.slug)

    return render(request, "village/forum_detail.html", {
        "topic": topic,
        "replies": replies,
        "form": form,
    })