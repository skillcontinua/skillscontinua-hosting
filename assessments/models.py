# File path: C:\hosting\skillscontinua_hosting\assessments\models.py
from django.db import models
from django.conf import settings
from vocational.models import TradeCourse, TradeModule, TradeLesson


class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ("formative", "Periodic Knowledge Check (Lesson Checkpoint)"),
        ("module_test", "Module Proficiency Test"),
        ("scenario_exam", "Real-Life Diagnostic / Field Scenario Test"),
        ("final_exam", "Tier / Final Certification Capstone Exam"),
    ]

    TIER_CHOICES = TradeCourse.TIER_CHOICES

    title = models.CharField(max_length=255)
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_1",
        help_text="Assessment tier: Tier 1 (Readiness), Tier 2 (Proficiency), or Tier 3 (Mastery)",
    )
    trade_course = models.ForeignKey(
        TradeCourse, related_name="quizzes", on_delete=models.CASCADE, null=True, blank=True
    )
    trade_module = models.ForeignKey(
        TradeModule, related_name="quizzes", on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.ForeignKey(
        TradeLesson, related_name="quizzes", on_delete=models.CASCADE, null=True, blank=True
    )
    instructions = models.TextField(
        blank=True,
        help_text="Clear instructions, scenario context, and rules before starting the test",
    )
    quiz_type = models.CharField(
        max_length=20, choices=QUIZ_TYPE_CHOICES, default="formative"
    )
    passing_score_percentage = models.PositiveIntegerField(
        default=75,
        help_text="Recommended: 70–75% for Tier 1/2, 80% for Tier 3 Capstone",
    )
    time_limit_minutes = models.PositiveIntegerField(
        default=20,
        help_text="Suggested time limit in minutes (0 = untimed for low-bandwidth flexibility)",
    )

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ["tier", "id"]

    def __str__(self):
        return f"[{self.get_tier_display()}] {self.title} ({self.get_quiz_type_display()})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    is_scenario_question = models.BooleanField(
        default=False,
        help_text="True if this question tests real-life troubleshooting, safety judgment, or client quoting",
    )
    text = models.TextField(help_text="Scenario or question text")
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    )
    explanation = models.TextField(
        blank=True,
        help_text="Clear field explanation shown after submission to reinforce retentive learning",
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(TradeLesson, blank=True)
    tier_1_completed = models.BooleanField(default=False)
    tier_2_completed = models.BooleanField(default=False)
    tier_3_completed = models.BooleanField(default=False)
    overall_progress_percentage = models.FloatField(default=0.0)
    last_activity = models.DateTimeField(auto_now=True)
    is_active_student = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "User Progress"
        unique_together = ("user", "trade_course")

    def __str__(self):
        return f"{self.user.username} - {self.trade_course.title} ({self.overall_progress_percentage}%)"


class Certificate(models.Model):
    TIER_CHOICES = TradeCourse.TIER_CHOICES

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier_3",
        help_text="Credential tier awarded (Tier 1 Readiness, Tier 2 Proficiency, or Tier 3 Master Credential)",
    )
    certificate_code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Cryptographic unique verification hash/code",
    )
    final_score = models.FloatField()
    grade_classification = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., Distinction (90%+), Merit (85–89%), Pass (80–84%)",
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    performance_summary = models.TextField(
        help_text="Detailed assessment breakdown backing this credential"
    )
    qr_code_url = models.URLField(blank=True, null=True)
    is_revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"Verified Certificate [{self.certificate_code}] ({self.get_tier_display()}) - {self.user.username}"


class CompetencyTranscript(models.Model):
    """
    Official itemized transcript detailing module scores, practical scenarios passed,
    and verified field competencies for employers, NGOs, governments, and manufacturers.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    certificate = models.OneToOneField(
        Certificate,
        related_name="transcript",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    transcript_code = models.CharField(max_length=100, unique=True)
    total_hours_completed = models.PositiveIntegerField(default=0)
    tier_1_score = models.FloatField(null=True, blank=True)
    tier_2_score = models.FloatField(null=True, blank=True)
    tier_3_score = models.FloatField(null=True, blank=True)
    verified_competencies = models.TextField(
        help_text="Itemized list of practical field skills, safety checks, and diagnostic scenarios mastered"
    )
    instructor_or_system_remarks = models.TextField(blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcript [{self.transcript_code}] - {self.user.username} ({self.trade_course.title})"


class DropoutTestimonial(models.Model):
    """
    Issued when a student pauses or exits early but is financially up to date,
    certifying the exact practical competencies acquired up to that point.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    testimonial_code = models.CharField(max_length=100, unique=True)
    modules_completed_count = models.PositiveIntegerField()
    financial_standing = models.CharField(max_length=50, default="Up to Date")
    issued_at = models.DateTimeField(auto_now_add=True)
    skills_mastered_summary = models.TextField(
        help_text="Competencies acquired prior to exit"
    )

    def __str__(self):
        return f"Testimonial [{self.testimonial_code}] for {self.user.username}"