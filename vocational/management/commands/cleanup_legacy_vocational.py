# File path:
# C:\hosting\skillscontinua_hosting\vocational\management\commands\cleanup_legacy_vocational.py
from django.core.management.base import BaseCommand
from vocational.models import TradeCategory, TradeCourse


CANONICAL_CATEGORY_SLUGS = {
    "solar-renewable-energy",
    "smartphone-repair",
    "laptop-pc-hardware-repair",
    "cctv-intercom-network-installation",
    "barbing-hairdressing-makeup-nail-art",
}

CANONICAL_COURSE_SLUGS = {
    # Solar (Tiers 1-3)
    "off-grid-solar-tier-1-foundation",
    "off-grid-solar-tier-2-proficiency",
    "off-grid-solar-tier-3-professional",
    # Smartphone Repair (Tiers 1-3)
    "smartphone-repair-tier-1-foundation",
    "smartphone-repair-tier-2-proficiency",
    "smartphone-repair-tier-3-professional",
    # Laptop & PC Repair (Tiers 1-3)
    "laptop-repair-tier-1-foundation",
    "laptop-repair-tier-2-proficiency",
    "laptop-repair-tier-3-professional",
    # CCTV, Intercom & Network (Tiers 1-3)
    "cctv-intercom-network-tier-1-foundation",
    "cctv-intercom-network-tier-2-proficiency",
    "cctv-intercom-network-tier-3-professional",
    # Beauty & Grooming (Tiers 1-3)
    "beauty-grooming-tier-1-foundation",
    "beauty-grooming-tier-2-proficiency",
    "beauty-grooming-tier-3-professional",
}


class Command(BaseCommand):
    help = "Removes legacy non-3-tier vocational courses and non-canonical categories so only 3-tier tracks remain."

    def handle(self, *args, **options):
        legacy_courses = TradeCourse.objects.exclude(slug__in=CANONICAL_COURSE_SLUGS)
        course_count = legacy_courses.count()
        legacy_courses.delete()

        legacy_categories = TradeCategory.objects.exclude(slug__in=CANONICAL_CATEGORY_SLUGS)
        cat_count = legacy_categories.count()
        legacy_categories.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Removed {course_count} legacy course(s) and {cat_count} legacy category(ies). "
                "Only standardized 3-tier vocational tracks remain."
            )
        )