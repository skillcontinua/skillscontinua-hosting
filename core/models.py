# File path: C:\hosting\skillscontinua_hosting\core\models.py
from django.db import models

class BaseCourse(models.Model):
    LEVEL_CHOICES = [
        ('Foundation', 'Foundation / Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced / Professional')
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'), ('fr', 'French'), ('ig', 'Igbo'),
        ('sw', 'Swahili'), ('ar', 'Arabic'), ('es', 'Spanish'), ('pt', 'Portuguese')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    pillar = models.CharField(max_length=100, help_text="e.g., Agriculture, Business, IT, Education")
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Foundation')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    duration_hours = models.PositiveIntegerField(help_text="Estimated completion duration in hours")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} ({self.level} - {self.language.upper()})"


class BaseModule(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']


class BaseLesson(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    # The 10-Step Practical Mastery Structure
    learning_objectives = models.TextField(help_text="Step 2: Exact outcomes the learner will achieve")
    why_it_matters = models.TextField(help_text="Step 3: Connection to real life, employment, or business")
    core_explanation = models.TextField(help_text="Step 4: Clear, practical teaching content")
    visual_diagram_code = models.TextField(blank=True, null=True, help_text="Step 5: Optional Mermaid.js diagram code or visual note")
    step_by_step_guide = models.TextField(help_text="Step 6: Exact 4-8 tactical steps to execute the skill")
    real_life_scenario = models.TextField(help_text="Step 7: Lifetime scenario simulation & crisis handling")
    practice_activity = models.TextField(help_text="Step 8: Immediate hands-on task")
    downloadable_resource_url = models.URLField(blank=True, null=True, help_text="Step 10: Permanent offline PDF checklist/template")

    class Meta:
        abstract = True
        ordering = ['order']