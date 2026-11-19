# File path: C:\hosting\skillscontinua_hosting\pedagogy\management\commands\seed_pedagogy.py
from django.core.management.base import BaseCommand
from pedagogy.models import PedagogicCourse, PedagogicModule, PedagogicLesson

class Command(BaseCommand):
    help = 'Seeds foundational primary and secondary school curricula'

    def handle(self, *args, **kwargs):
        course, _ = PedagogicCourse.objects.get_or_create(
            slug='stem-foundations-junior',
            defaults={
                'title': 'Junior STEM & Basic Digital Literacy for Young Learners',
                'pillar': 'Pedagogy',
                'description': 'Foundational mathematics, basic science experiments, and introductory computer logic for students.',
                'level': 'Foundation',
                'duration_hours': 50,
                'is_featured': True
            }
        )
        mod, _ = PedagogicModule.objects.get_or_create(course=course, title='Module 1: Introduction to Logic & Numbers', order=1)
        PedagogicLesson.objects.get_or_create(
            module=mod,
            title='Understanding Cause, Effect, and Simple Algorithms',
            defaults={
                'order': 1,
                'learning_objectives': 'Introduce sequential thinking through real-world examples.',
                'why_it_matters': 'Logical reasoning is the bedrock of mathematics, science, and coding.',
                'core_explanation': 'An algorithm is simply a step-by-step recipe to achieve a goal.',
                'step_by_step_guide': '1. Define the goal.\n2. List actions in order.\n3. Test the sequence.',
                'real_life_scenario': 'Writing steps to plant a seed.',
                'practice_activity': 'Draft a 5-step morning routine flowchart.',
            }
        )
        self.stdout.write(self.style.SUCCESS("Pedagogy foundation courses seeded successfully!"))