# File path: C:\hosting\skillscontinua_hosting\andragogy\models.py
from django.db import models
from core.models import BaseCourse, BaseModule, BaseLesson

class AndragogicCourse(BaseCourse):
    estimated_startup_capital = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., ₦50,000 lean startup or Zero capital")
    target_income_potential = models.CharField(max_length=150, blank=True, null=True, help_text="e.g., ₦150k–₦500k per contract or 6-month harvest cycle")

class AndragogicModule(BaseModule):
    course = models.ForeignKey(AndragogicCourse, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class AndragogicLesson(BaseLesson):
    module = models.ForeignKey(AndragogicModule, related_name='lessons', on_delete=models.CASCADE)
    local_market_application = models.TextField(blank=True, null=True, help_text="How to price, source materials, and find customers locally")

    def __str__(self):
        return self.title