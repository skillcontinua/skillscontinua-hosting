from django.core.management.base import BaseCommand
from vocational.models import TradeCategory, TradeCourse, TradeModule, TradeLesson

class Command(BaseCommand):
    help = 'Seeds initial professional vocational courses into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding vocational courses...")

        # 1. Create Category
        solar_cat, _ = TradeCategory.objects.get_or_create(
            name="Renewable Energy & Solar",
            slug="renewable-energy-solar",
            description="Professional solar installation, inverter maintenance, and battery technology."
        )

        # 2. Create Course
        solar_course, _ = TradeCourse.objects.get_or_create(
            slug="solar-installation-mastery",
            defaults={
                'category': solar_cat,
                'title': "Solar Panel Installation & Business - Power Homes & Shops",
                'description': "Comprehensive training on photovoltaic systems, charge controllers, inverter wiring, and maintenance.",
                'level': 'Foundation',
                'duration_hours': 80,
                'required_tools': "Multimeter, Wire strippers, Screw set, Solar panel meter, Insulation tape",
                'safety_guidelines': "Always disconnect DC breaker before touching terminals. Use insulated gloves.",
                'is_featured': True
            }
        )

        # 3. Create Module
        module_one, _ = TradeModule.objects.get_or_create(
            trade_course=solar_course,
            title="Module 1: Fundamentals of Photovoltaic Systems",
            order=1
        )

        # 4. Create Lesson following the 10-Step Framework
        TradeLesson.objects.get_or_create(
            module=module_one,
            title="Understanding Solar Irradiation and Panel Wiring",
            defaults={
                'order': 1,
                'learning_objectives': "By the end of this lesson, you will calculate daily energy load and configure series vs parallel connections.",
                'why_it_matters': "Correct wiring prevents voltage mismatch, protects inverters from blowing up, and ensures 24/7 power for clients.",
                'core_explanation': "Solar panels convert sunlight to DC electricity. Connecting panels in series increases voltage, while parallel increases current.",
                'step_by_step_field_guide': "1. Measure open-circuit voltage with multimeter.\n2. Mount aluminum brackets securely on roof.\n3. Connect positive to positive for parallel, or positive to negative for series.\n4. Route DC cables safely through conduit pipes.",
                'real_life_scenario': "A client's inverter shuts down under heavy air-conditioner load at night. Troubleshoot battery bank depth of discharge and array output.",
                'practice_activity': "Draw a wiring diagram for a 24V system using two 12V batteries and two 300W solar panels.",
                'downloadable_resource_url': "https://app.skillscontinua.com/resources/solar-wiring-cheat-sheet.pdf"
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample vocational course data!"))