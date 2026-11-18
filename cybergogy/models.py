# File path: C:\hosting\skillscontinua_hosting\cybergogy\models.py
from django.db import models
from core.models import BaseCourse, BaseModule, BaseLesson

class CybergogicCourse(BaseCourse):
    software_stack = models.CharField(max_length=255, help_text="e.g., Python, AWS, ChatGPT, Blender, Excel, Linux")
    certification_alignment = models.CharField(max_length=150, blank=True, null=True, help_text="e.g., CompTIA A+, Cisco CCNA, AWS Cloud Practitioner")

class CybergogicModule(BaseModule):
    course = models.ForeignKey(CybergogicCourse, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CybergogicLesson(BaseLesson):
    module = models.ForeignKey(CybergogicModule, related_name='lessons', on_delete=models.CASCADE)
    code_or_prompt_sandbox = models.TextField(blank=True, null=True, help_text="Copy-paste AI prompt, CLI command, or code snippet for the lab")

    def __str__(self):
        return self.title