# File path: C:\hosting\skillscontinua_hosting\vocational\models.py
from django.db import models


class TradeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Solar & Renewable Energy
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo_image = models.ImageField(
        upload_to="vocational/logos/",
        blank=True,
        null=True,
        help_text="Trade emblem or partner-ready category logo",
    )
    logo_svg_or_icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon class or short badge label for the trade",
    )

    class Meta:
        verbose_name_plural = "Trade Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TradeCourse(models.Model):
    LEVEL_CHOICES = [
        ("Foundation", "Foundation / Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced / Professional"),
    ]

    TIER_CHOICES = [
        ("tier_1", "Tier 1 — Free Foundation & Value Preview"),
        ("tier_2", "Tier 2 — Affordable Practical Proficiency"),
        ("tier_3", "Tier 3 — Professional Mastery & QR Credential"),
    ]

    category = models.ForeignKey(
        TradeCategory, related_name="trade_courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    banner_image = models.ImageField(
        upload_to="vocational/courses/",
        blank=True,
        null=True,
        help_text="Optional visual banner or setup diagram image for this course tier",
    )

    # 3-Tier & Proficiency Alignment
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_1",
        help_text="Monetization & mastery tier: Tier 1 (Free), Tier 2 (Affordable Proficiency), Tier 3 (Professional + QR Credential)",
    )
    is_free_tier = models.BooleanField(
        default=True,
        help_text="True for Tier 1 appetite-building content; False for paid Tier 2/3 tracks",
    )
    level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default="Foundation"
    )
    duration_hours = models.PositiveIntegerField(
        help_text="Practical training duration in hours"
    )
    credential_awarded = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g., Tier 1 Readiness Record, Tier 2 Proficiency Certificate, or Tier 3 Master QR Certificate & Transcript",
    )

    # Trade Readiness & Field Standards
    required_tools = models.TextField(
        help_text="List of tools, meters, crimpers, and PPE required for this trade"
    )
    safety_guidelines = models.TextField(
        help_text="Critical safety protocols, lockout/isolation rules, and hazard controls"
    )
    field_tips_summary = models.TextField(
        blank=True,
        help_text="High-value real-world 'trap avoidance' and self-employment tips for learners",
    )
    course_glossary_overview = models.TextField(
        blank=True,
        help_text="End-of-course or early-access glossary & reference guide covering course scope, duration, tools, terms, and safety",
    )

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tier", "title"]

    def __str__(self):
        return f"[{self.get_tier_display()}] {self.title}"


class TradeModule(models.Model):
    TIER_CHOICES = TradeCourse.TIER_CHOICES

    trade_course = models.ForeignKey(
        TradeCourse, related_name="modules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_1",
        help_text="Indicates which tier this module belongs to",
    )
    summary = models.TextField(
        blank=True,
        help_text="Module overview, competency outcome, and assessment checkpoint notes",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.trade_course.title} - {self.title}"


class TradeLesson(models.Model):
    module = models.ForeignKey(
        TradeModule, related_name="lessons", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    estimated_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Estimated study and practical walkthrough time in minutes",
    )
    is_free_preview = models.BooleanField(
        default=False,
        help_text="Allow free preview access even when attached to a paid tier course",
    )

    # Practical Field Mastery Structure
    learning_objectives = models.TextField()
    why_it_matters = models.TextField()
    core_explanation = models.TextField()
    step_by_step_field_guide = models.TextField(
        help_text="Exact physical operations, tables, and step-by-step instructions"
    )
    safety_and_traps = models.TextField(
        blank=True,
        help_text="Lesson-specific safety warnings and 'real-life trap' field tips",
    )
    diagram_or_visual_guide = models.TextField(
        blank=True,
        help_text="Diagram descriptions, schematic callouts, image references, or video/audio walkthrough notes",
    )
    visual_image = models.ImageField(
        upload_to="vocational/lessons/",
        blank=True,
        null=True,
        help_text="Optional diagram, wiring chart, or bench setup image for this lesson",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Video walkthrough or field demonstration URL",
    )
    real_life_scenario = models.TextField(
        help_text="Simulated workplace, client, or fault-diagnostic problem solving"
    )
    practice_activity = models.TextField()
    checkpoint_questions = models.TextField(
        blank=True,
        help_text="Quick self-check or quiz prompt tied to this lesson before moving forward",
    )
    downloadable_resource_url = models.URLField(
        blank=True, null=True, help_text="PDF blueprint, checklist, or cheat sheet URL"
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class TradeGlossaryTerm(models.Model):
    GLOSSARY_CATEGORY_CHOICES = [
        ("general", "General & Units"),
        ("equipment", "Equipment & Components"),
        ("tools", "Tools & Testing Instruments"),
        ("safety", "Safety, Protection & Standards"),
        ("business", "Sizing, Commissioning & Business"),
    ]

    course = models.ForeignKey(
        TradeCourse,
        related_name="glossary_terms",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Optional course link; leave blank to make term available across all trades",
    )
    category = models.ForeignKey(
        TradeCategory,
        related_name="glossary_terms",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    topic_group = models.CharField(
        max_length=30,
        choices=GLOSSARY_CATEGORY_CHOICES,
        default="general",
    )
    term = models.CharField(
        max_length=120,
        help_text="Term or acronym (e.g., EPDM, MC4, Voc, DoD, MPPT, SPD)",
    )
    full_expansion = models.CharField(
        max_length=255,
        blank=True,
        help_text="Full form if an acronym (e.g., Ethylene Propylene Diene Monomer)",
    )
    definition = models.TextField(
        help_text="Clear, plain-language explanation for learners"
    )
    field_application = models.TextField(
        blank=True,
        help_text="How this term applies on site, in sizing, or in avoiding mistakes",
    )
    available_from_tier_1 = models.BooleanField(
        default=True,
        help_text="Show in Tier 1 starter/early glossary to motivate learners early",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "term"]

    def __str__(self):
        return f"{self.term} — {self.full_expansion or self.get_topic_group_display()}"