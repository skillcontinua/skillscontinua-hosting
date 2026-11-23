# File path: C:\hosting\skillscontinua_hosting\core\models.py
from django.db import models


class BaseCourse(models.Model):
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

    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("fr", "French"),
        ("ig", "Igbo"),
        ("sw", "Swahili"),
        ("ar", "Arabic"),
        ("es", "Spanish"),
        ("pt", "Portuguese"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    pillar = models.CharField(
        max_length=100, help_text="e.g., Agriculture, Business, IT, Education, Solar"
    )
    description = models.TextField()

    # 3-Tier Monetization & Credential Alignment
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_1",
        help_text="Tier 1 (Free preview), Tier 2 (Affordable proficiency), Tier 3 (Professional + QR credential)",
    )
    is_free_tier = models.BooleanField(
        default=True,
        help_text="True for Tier 1 free access; False for paid Tier 2/3 tracks",
    )
    credential_awarded = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g., Tier 1 Readiness Record, Tier 2 Proficiency Certificate, Tier 3 Master QR Certificate & Transcript",
    )

    level = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default="Foundation"
    )
    language = models.CharField(
        max_length=5, choices=LANGUAGE_CHOICES, default="en"
    )
    duration_hours = models.PositiveIntegerField(
        help_text="Estimated completion duration in hours"
    )

    # Readiness, Safety, Field Tips & Glossary Support
    required_tools = models.TextField(
        blank=True,
        help_text="Required tools, software, materials, or workspace setup for this course",
    )
    safety_guidelines = models.TextField(
        blank=True,
        help_text="Safety protocols, operational warnings, and risk controls",
    )
    field_tips_summary = models.TextField(
        blank=True,
        help_text="High-value practical tips and common 'real-life traps' to avoid",
    )
    course_glossary_overview = models.TextField(
        blank=True,
        help_text="End-of-course or early-access glossary and reference guide covering scope, terms, tools, and safety",
    )

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["tier", "title"]

    def __str__(self):
        return f"{self.title} [{self.get_tier_display()}] ({self.language.upper()})"


class BaseModule(models.Model):
    TIER_CHOICES = BaseCourse.TIER_CHOICES

    title = models.CharField(max_length=255)
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_1",
        help_text="Indicates which tier this module belongs to",
    )
    summary = models.TextField(
        blank=True,
        help_text="Module overview, practical outcomes, and assessment notes",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class BaseLesson(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    estimated_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Estimated study and hands-on practice time in minutes",
    )
    is_free_preview = models.BooleanField(
        default=False,
        help_text="Allow free preview access even within a paid tier course",
    )

    # Practical Mastery & Field Execution Structure
    learning_objectives = models.TextField(
        help_text="Exact measurable outcomes the learner will achieve"
    )
    why_it_matters = models.TextField(
        help_text="Connection to income, employability, safety, or real-world problem solving"
    )
    core_explanation = models.TextField(
        help_text="Clear, structured teaching content, concepts, and reference tables"
    )
    visual_diagram_code = models.TextField(
        blank=True,
        null=True,
        help_text="Optional Mermaid.js diagram code, schematic notes, image/video reference, or visual guide",
    )
    step_by_step_guide = models.TextField(
        help_text="Exact step-by-step execution procedure"
    )
    safety_and_traps = models.TextField(
        blank=True,
        help_text="Safety warnings and common real-life mistakes ('traps') to watch out for",
    )
    real_life_scenario = models.TextField(
        help_text="Simulated workplace, client, or fault-handling scenario"
    )
    practice_activity = models.TextField(
        help_text="Immediate hands-on exercise to reinforce retentive learning"
    )
    checkpoint_questions = models.TextField(
        blank=True,
        help_text="Quick self-test questions to verify understanding before advancing",
    )
    downloadable_resource_url = models.URLField(
        blank=True,
        null=True,
        help_text="Permanent offline PDF checklist, blueprint, or cheat sheet URL",
    )

    class Meta:
        abstract = True
        ordering = ["order", "id"]