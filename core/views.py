# File path: C:\hosting\skillscontinua_hosting\core\views.py
from django.shortcuts import render
from vocational.models import TradeCourse
from village.models import CommunityPost, MediaStream, ForumTopic, SocialChannel, MonetizationOffer


def home_view(request):
    context = {
        'featured_trades': TradeCourse.objects.filter(is_featured=True)[:6],
        'latest_posts': CommunityPost.objects.filter(is_published=True)[:3],
        'media_streams': MediaStream.objects.filter(is_featured=True)[:3],
        'forum_topics': ForumTopic.objects.all()[:3],
        'social_channels': SocialChannel.objects.filter(is_active=True),
        'monetization_offers': MonetizationOffer.objects.filter(is_active=True),
    }
    return render(request, 'core/home.html', context)