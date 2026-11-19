# C:\hosting\skillscontinua_hosting\village\management\commands\seed_cybergogy.py
from django.core.management.base import BaseCommand
from cybergogy.models import CybergogicCourse, CybergogicModule, CybergogicLesson

class Command(BaseCommand):
    help = 'Seeds software engineering and AI prompt engineering courses'

    def handle(self, *args, **kwargs):
        course, _ = CybergogicCourse.objects.get_or_create(
            slug='python-ai-software-engineering',
            defaults={
                'title': 'Python & AI Prompt Engineering for Full-Stack Developers',
                'pillar': 'Cybergogy & Tech',
                'description': 'Master Django, APIs, and AI-assisted coding to build scalable web apps.',
                'level': 'Intermediate',
                'language': 'en',
                'duration_hours': 100,
                'software_stack': 'Python, Django, PostgreSQL, Git, ChatGPT',
                'certification_alignment': 'Python Institute PCEP / AWS Cloud Practitioner',
                'is_featured': True
            }
        )
        mod, _ = CybergogicModule.objects.get_or_create(course=course, title='Module 1: Django Architecture & Models', order=1)
        CybergogicLesson.objects.get_or_create(
            module=mod,
            title='Building Scalable Modular Apps in Django 5.2',
            defaults={
                'order': 1,
                'learning_objectives': 'Structure multi-app Django projects for clean maintainability.',
                'why_it_matters': 'Modular design prevents spaghetti code and ensures long-term software health.',
                'core_explanation': 'Isolate apps by domain responsibility (accounts, vocational, assessments).',
                'step_by_step_guide': '1. Run startapp.\n2. Register in INSTALLED_APPS.\n3. Define models.\n4. Migrate.',
                'real_life_scenario': 'Refactor a monolithic script into a clean Django package.',
                'practice_activity': 'Create a new modular app for student progress tracking.',
                'code_or_prompt_sandbox': 'python manage.py startapp analytics'
            }
        )
        self.stdout.write(self.style.SUCCESS("Cybergogy courses seeded successfully!"))