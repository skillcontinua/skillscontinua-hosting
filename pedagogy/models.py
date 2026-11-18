# File path: C:\hosting\skillscontinua_hosting\pedagogy\models.py
from django.db import models
from core.models import BaseCourse, BaseModule, BaseLesson

class PedagogicCourse(BaseCourse):
    GRADE_CHOICES = [
        ('Primary', 'Primary School (Ages 6–11)'),
        ('Junior_Secondary', 'Junior Secondary (Ages 12–14)'),
        ('Senior_Secondary', 'Senior Secondary (Ages 15–18)'),
    ]
    grade_level = models.CharField(max_length=30, choices=GRADE_CHOICES, default='Primary')
    guardian_guidance_notes = models.TextField(blank=True, null=True, help_text="Notes for parents or teachers supervising the child")

class PedagogicModule(BaseModule):
    course = models.ForeignKey(PedagogicCourse, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class PedagogicLesson(BaseLesson):
    module = models.ForeignKey(PedagogicModule, related_name='lessons', on_delete=models.CASCADE)
    interactive_activity_hint = models.TextField(blank=True, null=True, help_text="Fun game, puzzle, or visual exercise for young learners")

    def __str__(self):
        return self.title