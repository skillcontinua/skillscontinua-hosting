# File path: C:\hosting\skillscontinua_hosting\assessments\models.py
from django.db import models
from django.conf import settings
from vocational.models import TradeCourse, TradeLesson


class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('formative', 'Periodic Knowledge Check'),
        ('module_test', 'Module Test'),
        ('final_exam', 'Final Certification Exam')
    ]
    
    title = models.CharField(max_length=255)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(TradeLesson, on_delete=models.CASCADE, null=True, blank=True)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, default='formative')
    passing_score_percentage = models.PositiveIntegerField(default=70)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"Quiz: {self.title} ({self.quiz_type})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(help_text="Scenario or question text")
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"Q: {self.text[:50]}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(TradeLesson, blank=True)
    overall_progress_percentage = models.FloatField(default=0.0)
    last_activity = models.DateTimeField(auto_now=True)
    is_active_student = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "User Progress"

    def __str__(self):
        return f"{self.user.username} - {self.trade_course.title} ({self.overall_progress_percentage}%)"


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    certificate_code = models.CharField(max_length=100, unique=True, help_text="Cryptographic unique verification hash")
    final_score = models.FloatField()
    issued_at = models.DateTimeField(auto_now_add=True)
    performance_summary = models.TextField(help_text="Detailed assessment breakdown backing this credential")
    qr_code_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Verified Certificate [{self.certificate_code}] - {self.user.username}"


class DropoutTestimonial(models.Model):
    """
    Issued when a student pauses or exits early but is financially up to date,
    certifying the exact practical competencies acquired up to that point.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_course = models.ForeignKey(TradeCourse, on_delete=models.CASCADE)
    testimonial_code = models.CharField(max_length=100, unique=True)
    modules_completed_count = models.PositiveIntegerField()
    financial_standing = models.CharField(max_length=50, default='Up to Date')
    issued_at = models.DateTimeField(auto_now_add=True)
    skills_mastered_summary = models.TextField(help_text="Competencies acquired prior to exit")

    def __str__(self):
        return f"Testimonial [{self.testimonial_code}] for {self.user.username}"