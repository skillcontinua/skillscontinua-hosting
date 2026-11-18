# File path: C:\hosting\skillscontinua_hosting\heutagogy\models.py
from django.db import models
from core.models import BaseCourse, BaseModule, BaseLesson

class HeutagogicCourse(BaseCourse):
    capstone_deliverable = models.TextField(help_text="Major portfolio piece, strategic plan, or research appraisal required to graduate")
    prerequisite_experience = models.CharField(max_length=255, blank=True, null=True)

class HeutagogicModule(BaseModule):
    course = models.ForeignKey(HeutagogicCourse, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class HeutagogicLesson(BaseLesson):
    module = models.ForeignKey(HeutagogicModule, related_name='lessons', on_delete=models.CASCADE)
    self_directed_research_prompt = models.TextField(blank=True, null=True, help_text="Open-ended inquiry challenge for independent exploration")

    def __str__(self):
        return self.title