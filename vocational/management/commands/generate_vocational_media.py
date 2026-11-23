# C:\hosting\skillscontinua_hosting\vocational\management\commands
from io import BytesIO
from pathlib import Path
import textwrap

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from vocational.models import TradeCategory, TradeCourse, TradeLesson


TRADE_THEMES = {
    "cctv-intercom-network": {
        "short": "CCTV & NET",
        "accent": (14, 116, 144),
        "secondary": (224, 242, 254),
        "tools": [
            "RJ45 Crimp Tool & LAN Tester",
            "PoE Switch, NVR & Camera Mounts",
            "BNC / Coax & Drip-Loop Kit",
            "Fluke / Cable Certifier & Labels",
        ],
    },
    "beauty-grooming-cosmetology": {
        "short": "BEAUTY & CARE",
        "accent": (157, 23, 77),
        "secondary": (252, 231, 243),
        "tools": [
            "Cordless Clippers, Trimmers & Guards",
            "Shears, Combs, Section Clips & Brushes",
            "EPA Disinfectant, Barbicide & Towels",
            "Makeup Brushes, Palettes & Nail Drill",
        ],
    },
    "solar-renewable-energy": {
        "short": "OFF-GRID SOLAR",
        "accent": (180, 83, 9),
        "secondary": (254, 243, 199),
        "tools": [
            "Digital Clamp Multimeter (AC/DC)",
            "MC4 Crimper & PV String Tester",
            "DC MCB, SPD & Battery Busbars",
            "Compass, Sun-Path & Torque Wrenches",
        ],
    },
    "smartphone-repair": {
        "short": "PHONE REPAIR",
        "accent": (30, 64, 175),
        "secondary": (219, 234, 254),
        "tools": [
            "ESD Mat, Wrist Strap & Plastic Spudgers",
            "Precision Torx/Pentalobe/Tri-Point Drivers",
            "USB Power/Amp Meter & Heat Pad",
            "IPA, Adhesives & Containment Bucket",
        ],
    },
    "laptop-pc-hardware-repair": {
        "short": "PC & LAPTOP",
        "accent": (21, 128, 61),
        "secondary": (220, 252, 231),
        "tools": [
            "ESD Mat, Ground Strap & Driver Kit",
            "Thermal Paste, Pads & Fan Brush",
            "RAM (SO-DIMM/DIMM) & NVMe/SATA SSDs",
            "Multimeter, DC/PD Tester & Boot USB",
        ],
    },
}


def _load_font(size: int, bold: bool = False):
    candidates = (
        [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def _render_card(
    width: int,
    height: int,
    badge_text: str,
    title_text: str,
    subtitle_text: str,
    bullets: list[str],
    accent: tuple[int, int, int],
    soft_bg: tuple[int, int, int],
) -> ContentFile:
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Top accent bar
    header_h = max(68, int(height * 0.18))
    draw.rectangle([0, 0, width, header_h], fill=accent)

    # Subtle side accent stripe
    stripe_w = max(10, int(width * 0.015))
    draw.rectangle([0, header_h, stripe_w, height], fill=accent)

    font_badge = _load_font(max(14, int(header_h * 0.34)), bold=True)
    font_title = _load_font(max(20, int(height * 0.062)), bold=True)
    font_sub = _load_font(max(15, int(height * 0.042)), bold=False)
    font_body = _load_font(max(14, int(height * 0.038)), bold=False)

    # Badge pill in header
    pill_pad_x = 14
    pill_h = max(32, int(header_h * 0.56))
    pill_y = (header_h - pill_h) // 2
    draw.rounded_rectangle(
        [24, pill_y, 24 + len(badge_text) * 11 + pill_pad_x * 2, pill_y + pill_h],
        radius=8,
        fill=soft_bg,
    )
    draw.text((24 + pill_pad_x, pill_y + 6), badge_text, fill=accent, font=font_badge)

    cursor_y = header_h + 22
    left_x = stripe_w + 24
    usable_w = width - left_x - 28

    for line in textwrap.wrap(title_text, width=max(24, usable_w // 12))[:3]:
        draw.text((left_x, cursor_y), line, fill=(15, 23, 42), font=font_title)
        cursor_y += int(height * 0.072)

    if subtitle_text:
        for line in textwrap.wrap(subtitle_text, width=max(32, usable_w // 9))[:2]:
            draw.text((left_x, cursor_y), line, fill=(71, 85, 105), font=font_sub)
            cursor_y += int(height * 0.052)

    if bullets and cursor_y + 40 < height:
        cursor_y += 8
        box_top = cursor_y
        box_bottom = min(height - 20, box_top + len(bullets[:4]) * int(height * 0.056) + 18)
        if box_bottom > box_top + 28:
            draw.rounded_rectangle(
                [left_x, box_top, width - 24, box_bottom],
                radius=10,
                fill=soft_bg,
                outline=accent,
                width=1,
            )
            inner_y = box_top + 10
            for item in bullets[:4]:
                if inner_y + 18 > box_bottom:
                    break
                wrapped = textwrap.wrap(f"• {item}", width=max(34, usable_w // 8))[:1]
                for wline in wrapped:
                    draw.text((left_x + 14, inner_y), wline, fill=(30, 41, 59), font=font_body)
                    inner_y += int(height * 0.052)

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return ContentFile(buf.getvalue())


class Command(BaseCommand):
    help = "Generates local tool & trade PNG assets in MEDIA_ROOT and attaches them to categories, courses, and lessons."

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)

        cat_count = 0
        course_count = 0
        lesson_count = 0

        for cat in TradeCategory.objects.all().order_by("id"):
            theme = TRADE_THEMES.get(
                cat.slug,
                {
                    "short": cat.name[:14].upper(),
                    "accent": (30, 41, 59),
                    "secondary": (226, 232, 240),
                    "tools": ["Core Trade Tools & Safety Gear", "Diagnostic & Testing Kit"],
                },
            )
            accent = theme["accent"]
            soft_bg = theme["secondary"]
            tools = theme["tools"]

            logo_file = _render_card(
                width=512,
                height=512,
                badge_text=theme["short"],
                title_text=cat.name,
                subtitle_text="SkillsContinua Vocational Trade",
                bullets=tools,
                accent=accent,
                soft_bg=soft_bg,
            )
            cat.logo_image.save(f"vocational/categories/{cat.slug}-logo.png", logo_file, save=True)
            cat_count += 1

            courses = TradeCourse.objects.filter(category=cat).order_by("tier", "id")
            for course in courses:
                tier_label = course.get_tier_display() if hasattr(course, "get_tier_display") else course.tier.upper()
                course_tools = [
                    t.strip()
                    for t in (course.required_tools or "").split(",")
                    if t.strip()
                ][:4] or tools

                banner_file = _render_card(
                    width=1200,
                    height=420,
                    badge_text=f"{theme['short']} | {tier_label}",
                    title_text=course.title,
                    subtitle_text=f"Level: {course.level} • Duration: {course.duration_hours}h",
                    bullets=course_tools,
                    accent=accent,
                    soft_bg=soft_bg,
                )
                course.banner_image.save(
                    f"vocational/courses/{course.slug}-banner.png",
                    banner_file,
                    save=True,
                )
                course_count += 1

                lessons = TradeLesson.objects.filter(module__trade_course=course).order_by(
                    "module__order", "order", "id"
                )
                for idx, lesson in enumerate(lessons, start=1):
                    visual_bullets = course_tools[:3] + [
                        f"Est. Time: {lesson.estimated_minutes} mins"
                    ]
                    lesson_file = _render_card(
                        width=960,
                        height=540,
                        badge_text=f"{theme['short']} • {tier_label}",
                        title_text=lesson.title,
                        subtitle_text=lesson.module.title,
                        bullets=visual_bullets,
                        accent=accent,
                        soft_bg=soft_bg,
                    )
                    lesson.visual_image.save(
                        f"vocational/lessons/{course.slug}-lesson-{idx:02d}.png",
                        lesson_file,
                        save=True,
                    )
                    lesson_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated and attached media in {media_root}: "
                f"{cat_count} category logos, {course_count} course banners, {lesson_count} lesson visuals."
            )
        )