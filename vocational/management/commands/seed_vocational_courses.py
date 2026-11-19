# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_vocational_courses.py
from django.core.management.base import BaseCommand
from vocational.models import TradeCategory, TradeCourse, TradeModule, TradeLesson


class Command(BaseCommand):
    help = 'Seeds high-demand self-employment vocational courses with 10-step practical frameworks'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding high-demand self-employment vocational courses...")

        # --- 1. CATEGORY: Renewable Energy ---
        solar_cat, _ = TradeCategory.objects.get_or_create(
            slug="renewable-energy-solar",
            defaults={
                'name': "Renewable Energy & Solar",
                'description': "Professional solar installation, inverter maintenance, and battery bank design."
            }
        )

        solar_course, _ = TradeCourse.objects.get_or_create(
            slug="solar-installation-mastery",
            defaults={
                'category': solar_cat,
                'title': "Solar + Inverter Installation & Business Mastery",
                'description': "Comprehensive training on photovoltaic systems, hybrid inverters, lithium/tubular battery banks, and load auditing for homes and shops.",
                'level': 'Foundation',
                'duration_hours': 80,
                'required_tools': "Digital Multimeter, Clamp Meter, Wire Strippers, Crimping Tool, Insulated Screwdriver Set",
                'safety_guidelines': "Always disconnect DC and AC breakers before touching terminals. Wear insulated gloves and eye protection.",
                'is_featured': True
            }
        )

        solar_mod, _ = TradeModule.objects.get_or_create(
            trade_course=solar_course,
            title="Module 1: Load Auditing & Photovoltaic Wiring",
            order=1
        )

        TradeLesson.objects.get_or_create(
            module=solar_mod,
            title="Calculating Client Energy Load & Series/Parallel Array Wiring",
            defaults={
                'order': 1,
                'learning_objectives': "Calculate daily watt-hour consumption and configure series vs parallel panel strings safely.",
                'why_it_matters': "Accurate load sizing prevents inverter overload and premature battery failure.",
                'core_explanation': "Series connections sum voltage while keeping current constant; parallel connections sum current while keeping voltage constant.",
                'step_by_step_field_guide': "1. List all client appliances and wattage.\n2. Multiply wattage by daily usage hours.\n3. Verify inverter MPPT voltage window.\n4. Measure open-circuit voltage (Voc) with multimeter before connecting to controller.",
                'real_life_scenario': "A retail shop wants to run 4 LED bulbs, 2 fans, a POS terminal, and a CCTV DVR for 10 hours overnight. Size the battery bank.",
                'practice_activity': "Draft a complete wiring schematic for a 3.5kVA 24V hybrid inverter system.",
                'downloadable_resource_url': "https://app.skillscontinua.com/resources/solar-wiring-sheet.pdf"
            }
        )

        # --- 2. CATEGORY: Electronics, Phone & Laptop Repair ---
        tech_repair_cat, _ = TradeCategory.objects.get_or_create(
            slug="phone-laptop-repair",
            defaults={
                'name': "Phone & Laptop Hardware Repair",
                'description': "Chip-level diagnostics, screen replacement, charging port micro-soldering, and OS troubleshooting."
            }
        )

        phone_course, _ = TradeCourse.objects.get_or_create(
            slug="smartphone-laptop-repair-mastery",
            defaults={
                'category': tech_repair_cat,
                'title': "Smartphone & Laptop Hardware Repair + Micro-Soldering",
                'description': "Diagnose dead motherboards, replace cracked LCD/OLED screens, swap laptop batteries/keyboards, and launch a high-margin repair kiosk.",
                'level': 'Intermediate',
                'duration_hours': 75,
                'required_tools': "Hot Air Rework Station, Precision Soldering Iron, Digital Multimeter, Precision Screwdriver Kit, Isopropyl Alcohol",
                'safety_guidelines': "Wear an anti-static wrist strap. Disconnect internal battery connectors before probing logic boards.",
                'is_featured': True
            }
        )

        phone_mod, _ = TradeModule.objects.get_or_create(
            trade_course=phone_course,
            title="Module 1: Screen Replacement & Charging Circuit Diagnostics",
            order=1
        )

        TradeLesson.objects.get_or_create(
            module=phone_mod,
            title="Safe LCD Separation & Charging Port Micro-Soldering",
            defaults={
                'order': 1,
                'learning_objectives': "Safely separate damaged screens and replace Type-C/Lightning charging ports without lifting board pads.",
                'why_it_matters': "Screen and charging port repairs account for over 70% of daily walk-in repair revenue.",
                'core_explanation': "Controlled heat softens factory adhesive without damaging underlying display flex cables or neighboring SMD capacitors.",
                'step_by_step_field_guide': "1. Pre-heat separator pad to 80°C.\n2. Gently lift glass edge with suction cup and plastic pry card.\n3. Disconnect battery flex first, then display flex.\n4. Test replacement screen thoroughly before applying B-7000 frame adhesive.",
                'real_life_scenario': "A student brings a laptop that powers on with fans spinning but shows no display on the built-in screen. Test via external HDMI.",
                'practice_activity': "Desolder and cleanly resolder a Type-C charging port on a practice motherboard.",
                'downloadable_resource_url': "https://app.skillscontinua.com/resources/phone-laptop-repair-guide.pdf"
            }
        )

        # --- 3. CATEGORY: Security Systems & Networking ---
        cctv_cat, _ = TradeCategory.objects.get_or_create(
            slug="cctv-intercom-networking",
            defaults={
                'name': "CCTV, Intercom & Network Installation",
                'description': "Analog HD & IP camera deployment, office intercoms, structured LAN cabling, and remote mobile viewing setup."
            }
        )

        cctv_course, _ = TradeCourse.objects.get_or_create(
            slug="cctv-intercom-network-installation",
            defaults={
                'category': cctv_cat,
                'title': "CCTV Surveillance, Intercom & Office Network Installation",
                'description': "Master indoor/outdoor camera mounting, BNC & RJ45 crimping, DVR/NVR configuration, PABX intercoms, and remote smartphone monitoring.",
                'level': 'Foundation',
                'duration_hours': 60,
                'required_tools': "RJ45/BNC Crimping Tool, Network Cable Tester, Rotary Hammer Drill, Fish Tape, Ladder",
                'safety_guidelines': "Verify wall routes for live electrical conduits before drilling. Secure ladders on level ground.",
                'is_featured': True
            }
        )

        cctv_mod, _ = TradeModule.objects.get_or_create(
            trade_course=cctv_course,
            title="Module 1: Structured Cabling, Camera Mounting & DVR Setup",
            order=1
        )

        TradeLesson.objects.get_or_create(
            module=cctv_mod,
            title="Crimping Cat6/Coaxial Cables & Configuring Remote Mobile View",
            defaults={
                'order': 1,
                'learning_objectives': "Terminate T568B RJ45 connectors, eliminate video ground-loop interference, and link DVRs to client phones.",
                'why_it_matters': "Clean terminations prevent flickering video feeds and costly callback visits.",
                'core_explanation': "IP cameras transmit power and data over a single Cat6 cable via PoE switches, simplifying commercial installations.",
                'step_by_step_field_guide': "1. Strip 2cm of Cat6 outer jacket without nicking twisted pairs.\n2. Arrange wires in T568B order (White-Orange, Orange, White-Green, Blue, White-Blue, Green, White-Brown, Brown).\n3. Crimp firmly and verify all 8 pins with a cable tester.\n4. Enable P2P cloud access on NVR and scan QR code on client smartphone.",
                'real_life_scenario': "A warehouse owner needs 8 night-vision cameras covering loading bays with 30 days of continuous recording. Calculate hard drive storage.",
                'practice_activity': "Crimp two Cat6 patch cords and verify zero crosstalk on a LAN tester.",
                'downloadable_resource_url': "https://app.skillscontinua.com/resources/cctv-network-checklist.pdf"
            }
        )

        # --- 4. CATEGORY: Beauty, Grooming & Personal Care ---
        beauty_cat, _ = TradeCategory.objects.get_or_create(
            slug="beauty-grooming-cosmetology",
            defaults={
                'name': "Barbing, Hairdressing, Makeup & Nail Art",
                'description': "High-demand personal grooming, precision fading, wig installation, bridal makeup, and acrylic/gel nail artistry."
            }
        )

        beauty_course, _ = TradeCourse.objects.get_or_create(
            slug="barbing-hairdressing-makeup-nails-pro",
            defaults={
                'category': beauty_cat,
                'title': "Professional Barbing, Hairdressing, Makeup & Nail Technology",
                'description': "Master precision clipper fades, frontal wig installation, flawless bridal makeup, and gel/acrylic nail extensions with strict salon hygiene.",
                'level': 'Foundation',
                'duration_hours': 90,
                'required_tools': "Cordless Clippers & Trimmers, Barbicide Disinfectant Jar, Ring Light, Makeup Brush & Palette Kit, UV/LED Nail Lamp & Drill",
                'safety_guidelines': "Sanitize clippers, combs, and cuticle nippers between every client to prevent skin and fungal infections.",
                'is_featured': True
            }
        )

        beauty_mod, _ = TradeModule.objects.get_or_create(
            trade_course=beauty_course,
            title="Module 1: Precision Grooming, Hygiene & Client Retention",
            order=1
        )

        TradeLesson.objects.get_or_create(
            module=beauty_mod,
            title="Clipper Fade Blending, Salon Sanitation & Bridal/Nail Prep",
            defaults={
                'order': 1,
                'learning_objectives': "Execute seamless skin-to-crown clipper fades, prep natural nails safely, and sanitize tools to clinical standards.",
                'why_it_matters': "Visible hygiene and consistent finishing turn first-time walk-ins into loyal weekly clients.",
                'core_explanation': "Guideline creation using closed-to-open lever adjustments creates smooth tonal transitions without harsh lines.",
                'step_by_step_field_guide': "1. Spray clipper blades with disinfectant and brush clean.\n2. Establish initial bald guideline with trimmer.\n3. Open clipper lever halfway and blend 1cm above guideline.\n4. Finish hairline edge cleanly and apply soothing aftershave antiseptic.",
                'real_life_scenario': "A bridal party books makeup, wig styling, and gel nails for 4 people starting at 6:00 AM. Create a timed workstation schedule.",
                'practice_activity': "Practice a 3-guard taper blend on a mannequin head and document tool sterilization steps.",
                'downloadable_resource_url': "https://app.skillscontinua.com/resources/salon-hygiene-pricing-kit.pdf"
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all 4 high-demand self-employment vocational courses!"))