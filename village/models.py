# File path: C:\hosting\skillscontinua_hosting\village\models.py
from django.db import models
from django.conf import settings


class CommunityPost(models.Model):
    """SEO Blog & Educational Articles to drive organic search traffic."""
    CATEGORY_CHOICES = [
        ('blog', 'Educational Blog & Guides'),
        ('success_story', 'Artisan & Graduate Success Story'),
        ('industry_news', 'Industry & Tech Updates'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='blog')
    summary = models.TextField(help_text="Short hook for cards and SEO meta description")
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class MediaStream(models.Model):
    """Short-form Reels (TikTok/Shorts) and Low-Data Audio Podcasts."""
    MEDIA_TYPE_CHOICES = [
        ('reel', 'Short Video / TikTok Reel'),
        ('podcast', 'Audio Podcast Episode'),
        ('webinar', 'Live Workshop / Webinar Replay'),
    ]

    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='reel')
    description = models.TextField(blank=True)
    external_url = models.URLField(help_text="Link to TikTok, YouTube Shorts, Spotify, or direct MP3/MP4")
    duration_label = models.CharField(max_length=30, blank=True, help_text="e.g., 60 sec, 15 mins")
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_media_type_display()}] {self.title}"


class ForumTopic(models.Model):
    """Peer-to-peer discussion boards and mentor Q&A."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    pillar_tag = models.CharField(max_length=50, default='General', help_text="e.g., Solar, Coding, Business, Study Help")
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    topic = models.ForeignKey(ForumTopic, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_verified_mentor_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Forum Replies"
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.author.username} on {self.topic.title}"


class SocialChannel(models.Model):
    """Dynamic social & community links (WhatsApp, TikTok, YouTube, Telegram) editable in Admin."""
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp Community / Channel'),
        ('tiktok', 'TikTok Official'),
        ('youtube', 'YouTube Channel'),
        ('telegram', 'Telegram Group'),
        ('facebook', 'Facebook Community'),
        ('linkedin', 'LinkedIn Network'),
    ]

    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, unique=True)
    handle_or_label = models.CharField(max_length=100, help_text="e.g., Join our WhatsApp Trade Hub")
    url = models.URLField()
    follower_count_label = models.CharField(max_length=50, blank=True, help_text="e.g., 12K+ Learners")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_platform_display()} ({self.handle_or_label})"


class MonetizationOffer(models.Model):
    """Manageable pricing tiers, certification fees, and sponsored toolkits."""
    OFFER_TYPE_CHOICES = [
        ('membership', 'Pro Learner Membership'),
        ('certification', 'Verified QR Certificate & Assessment'),
        ('toolkit', 'Recommended Physical/Digital Toolkit (Affiliate)'),
        ('corporate', 'Corporate / NGO Bulk Sponsorship'),
    ]

    title = models.CharField(max_length=200)
    offer_type = models.CharField(max_length=30, choices=OFFER_TYPE_CHOICES)
    price_display = models.CharField(max_length=100, help_text="e.g., Free, ₦5,000 / Certificate, $15/mo")
    description = models.TextField()
    call_to_action_text = models.CharField(max_length=50, default="Get Started")
    action_url = models.CharField(max_length=255, default="/accounts/", help_text="Internal path or external checkout/affiliate link")
    is_highlighted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.price_display})"