# File path: C:\hosting\skillscontinua_hosting\village\management\commands\seed_village.py
from django.core.management.base import BaseCommand
from accounts.models import User
from village.models import CommunityPost, MediaStream, ForumTopic, SocialChannel, MonetizationOffer


class Command(BaseCommand):
    help = 'Seeds initial Village community, media, social channels, and monetization tiers'

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(is_superuser=True).first()

        # 1. Seed Social Channels (WhatsApp, TikTok, YouTube)
        SocialChannel.objects.get_or_create(
            platform='whatsapp',
            defaults={
                'handle_or_label': 'Join WhatsApp Daily Trade Alerts',
                'url': 'https://whatsapp.com/channel/skillscontinua',
                'follower_count_label': 'Low-Data Updates',
            }
        )
        SocialChannel.objects.get_or_create(
            platform='tiktok',
            defaults={
                'handle_or_label': '@SkillsContinua 60s Field Tips',
                'url': 'https://www.tiktok.com/@skillscontinua',
                'follower_count_label': 'Quick Reels',
            }
        )
        SocialChannel.objects.get_or_create(
            platform='youtube',
            defaults={
                'handle_or_label': 'SkillsContinua Practical Labs',
                'url': 'https://www.youtube.com/@skillscontinua',
                'follower_count_label': 'Full Walkthroughs',
            }
        )

        # 2. Seed SEO Blog Articles
        CommunityPost.objects.get_or_create(
            slug='how-to-start-solar-business-with-minimal-capital',
            defaults={
                'title': 'How to Launch a Profitable Solar Maintenance Business in 30 Days',
                'author': admin_user,
                'category': 'blog',
                'summary': 'A practical breakdown of essential tools, client pricing models, and battery troubleshooting.',
                'content': 'Full practical guide on entering the renewable energy service sector...',
                'is_featured': True,
            }
        )
        CommunityPost.objects.get_or_create(
            slug='why-micro-credentials-beat-unverified-claims',
            defaults={
                'title': 'How QR-Verified Certificates & Dropout Testimonials Help Artisans Win Contracts',
                'author': admin_user,
                'category': 'success_story',
                'summary': 'Why employers and homeowners trust cryptographic skill verification before hiring.',
                'content': 'Detailed story on how verified competencies bridge the trust gap...',
                'is_featured': True,
            }
        )

        # 3. Seed Reels & Podcasts
        MediaStream.objects.get_or_create(
            title='60-Second Tip: Testing Inverter Battery Health with a Multimeter',
            defaults={
                'media_type': 'reel',
                'description': 'Quick field demonstration from our Aba vocational hub.',
                'external_url': 'https://www.tiktok.com/@skillscontinua',
                'duration_label': '0:58 Reel',
            }
        )
        MediaStream.objects.get_or_create(
            title='Episode 01: Turning Local Artisans into Digital Entrepreneurs',
            defaults={
                'media_type': 'podcast',
                'description': 'Low-bandwidth audio discussion on pricing, customer retention, and cooperative growth.',
                'external_url': 'https://app.skillscontinua.com/village/',
                'duration_label': '18 Min Audio',
            }
        )

        # 4. Seed Forum Topic
        if admin_user:
            ForumTopic.objects.get_or_create(
                slug='best-charge-controller-for-24v-shop-setup',
                defaults={
                    'title': 'MPPT vs PWM Charge Controller for a 24V Barber Shop Setup?',
                    'pillar_tag': 'Vocational / Solar',
                    'started_by': admin_user,
                    'body': 'Which controller gives better efficiency during cloudy days in Lagos/Port Harcourt?',
                    'is_pinned': True,
                }
            )

        # 5. Seed Monetization Tiers
        MonetizationOffer.objects.get_or_create(
            title='Open Access Learner',
            defaults={
                'offer_type': 'membership',
                'price_display': 'Free Forever',
                'description': 'Access foundational 10-step lessons, community forums, and WhatsApp study alerts.',
                'call_to_action_text': 'Start Learning Free',
                'is_highlighted': False,
            }
        )
        MonetizationOffer.objects.get_or_create(
            title='Verified Mastery & QR Credential',
            defaults={
                'offer_type': 'certification',
                'price_display': '₦5,000 / $5 per Exam',
                'description': 'Take proctored final exams, unlock cryptographic QR certificates, or request an official Dropout Testimonial.',
                'call_to_action_text': 'Get Certified',
                'is_highlighted': True,
            }
        )
        MonetizationOffer.objects.get_or_create(
            title='NGO & Corporate Workforce Sponsorship',
            defaults={
                'offer_type': 'corporate',
                'price_display': 'Custom Cohort Pricing',
                'description': 'Sponsor 50–5,000 youths across trades and tech with live progress dashboards and impact reporting.',
                'call_to_action_text': 'Partner With Us',
                'is_highlighted': False,
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Village Community, Social & Monetization data!"))