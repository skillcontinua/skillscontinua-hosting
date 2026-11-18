# File path: C:\hosting\skillscontinua_hosting\vocational\models.py
from django.db import models


class TradeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Solar & Renewable Energy, Automotive
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Trade Categories"

    def __str__(self):
        return self.name


class TradeCourse(models.Model):
    LEVEL_CHOICES = [
        ('Foundation', 'Foundation / Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced / Professional')
    ]

    category = models.ForeignKey(TradeCategory, related_name='trade_courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Foundation')
    duration_hours = models.PositiveIntegerField(help_text="Practical training duration in hours")
    required_tools = models.TextField(help_text="List of tools needed for this trade (e.g., Multimeter, Soldering iron)")
    safety_guidelines = models.TextField(help_text="Critical safety protocols for physical artisans")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Trade] {self.title}"


class TradeModule(models.Model):
    trade_course = models.ForeignKey(TradeCourse, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.trade_course.title} - {self.title}"


class TradeLesson(models.Model):
    module = models.ForeignKey(TradeModule, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    # The 10-Step Practical Field Structure
    learning_objectives = models.TextField()
    why_it_matters = models.TextField()
    core_explanation = models.TextField()
    step_by_step_field_guide = models.TextField(help_text="Exact physical operations instructions")
    real_life_scenario = models.TextField(help_text="Simulated workplace/client problem solving")
    practice_activity = models.TextField()
    downloadable_resource_url = models.URLField(blank=True, null=True, help_text="PDF blueprint/cheat sheet")

    def __str__(self):
        return self.title