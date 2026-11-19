# File path: C:\hosting\skillscontinua_hosting\andragogy\management\commands\seed_andragogy.py
from django.core.management.base import BaseCommand
from andragogy.models import AndragogicCourse, AndragogicModule, AndragogicLesson

class Command(BaseCommand):
    help = 'Seeds adult education and cooperative business courses'

    def handle(self, *args, **kwargs):
        course, _ = AndragogicCourse.objects.get_or_create(
            slug='cooperative-business-financial-literacy',
            defaults={
                'title': 'Cooperative Management & Artisan Financial Literacy',
                'pillar': 'Andragogy & Business',
                'description': 'Practical money management, cooperative savings groups, and pricing strategies for skilled artisans.',
                'level': 'Foundation',
                'duration_hours': 40,
                'is_featured': True
            }
        )
        mod, _ = AndragogicModule.objects.get_or_create(course=course, title='Module 1: Pricing for Profit & Cash Flow', order=1)
        AndragogicLesson.objects.get_or_create(
            module=mod,
            title='Calculating Labor, Materials, and Overhead',
            defaults={
                'order': 1,
                'learning_objectives': 'Accurately price repair and installation jobs to guarantee net profit.',
                'why_it_matters': 'Underpricing leads to business burnout and inability to restock tools.',
                'core_explanation': 'True job pricing = Material cost + Labor hours + Overhead allocation + Profit margin.',
                'step_by_step_guide': '1. List all parts needed.\n2. Estimate hours required.\n3. Add 15% contingency buffer.\n4. Present itemized quote to client.',
                'real_life_scenario': 'A solar client negotiates a 50% discount. How to hold firm without losing the job.',
                'practice_activity': 'Create a pricing template for a smartphone screen repair job.',
            }
        )
        self.stdout.write(self.style.SUCCESS("Andragogy business courses seeded successfully!"))