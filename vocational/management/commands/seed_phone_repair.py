# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_phone_repair.py
from django.core.management.base import BaseCommand
from vocational.models import (
    TradeCategory,
    TradeCourse,
    TradeModule,
    TradeLesson,
    TradeGlossaryTerm,
)
from assessments.models import Quiz, Question


class Command(BaseCommand):
    help = "Seeds the complete 3-tier Smartphone Hardware & Software Repair course, glossary, and quizzes."

    def handle(self, *args, **options):
        category, _ = TradeCategory.objects.update_or_create(
            slug="smartphone-repair",
            defaults={
                "name": "Smartphone Hardware & Software Repair",
                "description": (
                    "Dedicated mobile phone repair training covering ESD/LiPo battery safety, "
                    "non-destructive opening, screen/battery/charging-board replacement, firmware "
                    "flashing, board-level fault finding, and mobile repair shop operations."
                ),
            },
        )

        # =====================================================================
        # TIER 1 (FREE): SAFE DISASSEMBLY, DIAGNOSTICS & ESSENTIAL TOOLS
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 1: Diagnostics, ESD Safety & Safe Disassembly",
                "description": (
                    "FREE TIER: Master anti-static (ESD) safety, LiPo pouch battery protection, "
                    "USB current-meter triage, heat-assisted non-destructive phone opening, and core "
                    "mobile hardware terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Smartphone Diagnostics Readiness Record",
                "required_tools": (
                    "Precision Screwdriver Set (Phillips #000, Pentalobe P2, Tri-wing Y000), "
                    "Plastic Opening Picks & Nylon Spudgers, Suction Cup, Heating Pad / Heat Gun, "
                    "Isopropyl Alcohol (99% IPA), USB Voltage/Current Tester, ESD Wrist Strap & Mat"
                ),
                "safety_guidelines": (
                    "1. LIPO BATTERY FIRE SAFETY: Never use metal blades or sharp screwdrivers to pry glued pouch batteries.\n"
                    "2. ESD PROTECTION: Always ground yourself before touching exposed logic boards or camera sensors.\n"
                    "3. DISCONNECT BATTERY FLEX FIRST: Immediately unclip the battery FPC connector after opening the phone."
                ),
                "field_tips_summary": (
                    "Read the USB current meter before opening any phone: 0.00A, 0.05A, and 1.80A tell "
                    "you immediately whether the fault is port/cable, dead battery, or shorted board."
                ),
                "course_glossary_overview": (
                    "Covers ESD, LiPo Pouch Cell, FPC Connector, USB-C / Charging Sub-Board, "
                    "OLED vs. LCD, Digitizer, PMIC, Charging IC, and Bootloop."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Mobile Workshop Safety, USB Current Triage & Non-Destructive Opening",
                "tier": "tier_1",
                "summary": "Diagnose charging/power symptoms safely and open modern phones without cracking glass or tearing flex cables.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: LiPo Battery Safety, ESD Control & USB Current Meter Triage",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Prevent lithium-polymer battery punctures and electrostatic board damage.\n"
                    "- Use a USB voltage/current meter to diagnose dead or non-charging phones before opening."
                ),
                "why_it_matters": (
                    "Puncturing a smartphone battery causes instant thermal runaway and fire, while "
                    "reading a USB tester saves hours of unnecessary disassembly."
                ),
                "core_explanation": (
                    "A USB meter reveals power behavior immediately: ~0.00A points to a dirty/damaged "
                    "charging port or cable; low steady current (~0.05A–0.15A) often indicates a deeply "
                    "discharged battery or charging IC issue; normal fast-charge ramp (~1.5A–3.0A) with a "
                    "black screen points to display/backlight failure rather than a dead phone."
                ),
                "step_by_step_field_guide": (
                    "1. Put on ESD wrist strap and inspect phone frame for swelling, bends, or water indicators.\n"
                    "2. Clean lint carefully from the charging port using a non-conductive pick.\n"
                    "3. Plug into a known-good charger through a USB current tester and record Amps.\n"
                    "4. Log pre-existing cracks/faults and confirm client data backup notice."
                ),
                "safety_and_traps": (
                    "TRAP: Using metal tweezers inside a live charging port or prying swollen batteries with metal tools."
                ),
                "real_life_scenario": (
                    "A client brings a 'dead' phone; your USB tester shows 1.9A charging draw and vibration "
                    "on power press—confirming the board is alive and only the OLED display failed."
                ),
                "practice_activity": (
                    "Test 3 phones with a USB current meter and record their charging voltage, current draw, "
                    "and initial triage diagnosis."
                ),
                "checkpoint_questions": (
                    "1. What does 1.9A charging current on a phone with a black screen indicate?\n"
                    "2. Why must metal pry tools never be used against a LiPo pouch battery?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Heat-Assisted Opening, Screw Mapping & FPC Flex Disconnects",
                "estimated_minutes": 55,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Open rear-glass, frame-clip, and front-entry phones without tearing fingerprint/display flexes.\n"
                    "- Map micro-screws by exact position and release FPC connectors safely."
                ),
                "why_it_matters": (
                    "Modern phones hide fingerprint and volume flex ribbons directly under back covers; "
                    "inserting a pick too deep slices them instantly."
                ),
                "core_explanation": (
                    "Warm back glass evenly (~65°C–75°C) to soften adhesive, slide a plastic pick shallowly "
                    "(less than 2–3 mm around edges), eject the SIM tray before lifting mid-frames, "
                    "and unclip the battery FPC connector first using a nylon spudger."
                ),
                "step_by_step_field_guide": (
                    "1. Power off phone and eject the SIM card tray.\n"
                    "2. Warm perimeter adhesive evenly and insert plastic opening picks shallowly.\n"
                    "3. Lift cover slowly while checking for rear fingerprint/flash flex cables.\n"
                    "4. Unscrew shield plates onto a magnetic screw map and disconnect the battery FPC first."
                ),
                "safety_and_traps": (
                    "TRAP: Forcing a mid-frame off while the SIM tray is still inserted—it snaps the SIM reader."
                ),
                "real_life_scenario": (
                    "A mid-range Android phone refuses to separate at the side edge until you notice the "
                    "SIM tray was left in place."
                ),
                "practice_activity": (
                    "Disassemble and reassemble a practice smartphone while mapping every shield screw "
                    "and verifying all FPC connectors click securely."
                ),
                "checkpoint_questions": (
                    "1. Why must the SIM tray be removed before separating a phone mid-frame?\n"
                    "2. How deep should a plastic opening pick enter around a glued back cover?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Smartphone Safety, Triage & Opening Readiness Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify safe mobile opening, USB triage, and LiPo battery handling.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="A phone appears completely black, but when plugged into your USB current tester it pulls 1.85A and vibrates when the power button is held. What is the most likely fault?",
            option_a="A faulty display/OLED assembly or disconnected display flex rather than a dead motherboard",
            option_b="The SIM card is expired",
            option_c="The wall socket frequency is wrong",
            option_d="The rear glass adhesive is too cold",
            correct_answer="A",
            explanation="Strong normal charging current plus vibration confirms the motherboard is booting while the display output is absent.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="Which step prevents tearing a rear-mounted fingerprint sensor cable when opening a phone?",
            option_a="Push a metal blade 2 cm deep across the center of the back cover",
            option_b="Keep opening picks shallow (2–3 mm) along the perimeter and lift the cover slowly",
            option_c="Pull the back glass off rapidly without warming adhesive",
            option_d="Leave the battery connected while prying cables",
            correct_answer="B",
            explanation="Shallow perimeter entry and slow lifting prevent slicing delicate flex ribbons routed beneath the rear cover.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): SCREEN, BATTERY, CHARGING BOARD & FIRMWARE FLASHING
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 2: Screen, Battery, Charging Port & Software Flashing",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Replace LCD/OLED screens, pouch batteries, charging "
                    "sub-boards, speakers, and cameras cleanly; master test-before-gluing and official "
                    "firmware recovery/flashing."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 12,
                "credential_awarded": "Tier 2 Smartphone Hardware & Software Repair Certificate",
                "required_tools": (
                    "All Tier 1 tools plus B-7000/T-7000 Frame Adhesive, Screen Clamps/Elastic Bands, "
                    "Battery Pull-Tab Adhesive Strips, Soldering Iron & Flux, PC with USB Drivers & Flash Tools"
                ),
                "safety_guidelines": (
                    "1. TEST BEFORE GLUING: Always test replacement OLED/LCD displays loosely before applying B-7000/T-7000 adhesive.\n"
                    "2. SOLVENT CARE: Use minimal 99% IPA on battery pull tabs—never flood LCD backlights with alcohol.\n"
                    "3. FIRMWARE INTEGRITY: Match exact model/build numbers before flashing firmware to avoid hard-bricking."
                ),
                "field_tips_summary": (
                    "Clean every speck of broken glass from the frame lip before seating a new screen—"
                    "one tiny glass grain under an OLED panel will crack it the moment you clamp it."
                ),
                "course_glossary_overview": (
                    "Covers In-Cell LCD vs. Soft/Hard OLED, Frame Bezels, B-7000/T-7000 Adhesive, "
                    "Sub-Board / Dock Flex, Recovery/Fastboot/Download Mode, and Stock Firmware Flashing."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: Display, Battery & Charging Sub-Board Replacement",
                "tier": "tier_2",
                "summary": "Deliver factory-clean screen, battery, and charging replacements with zero adhesive lift.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: OLED/LCD Screen Replacement, Frame Prep & Test-Before-Glue Discipline",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Remove shattered glass/OLED assemblies safely and clean frame channels thoroughly.\n"
                    "- Test touch sensitivity, brightness, proximity sensor, and earpiece before gluing."
                ),
                "why_it_matters": (
                    "Suppliers void screen warranties once adhesive is applied or protective films are peeled—"
                    "testing first saves you from eating the cost of defective screens."
                ),
                "core_explanation": (
                    "Inspect the metal/plastic frame for bends and scrape away every shard of old glass "
                    "and adhesive. Connect the new display flex and battery, test multi-touch across all "
                    "corners, brightness slider, and proximity sensor, then apply a thin even bead of "
                    "frame adhesive and clamp gently."
                ),
                "step_by_step_field_guide": (
                    "1. Remove damaged display, transfer earpiece mesh/sensor brackets, and clean frame lip.\n"
                    "2. Connect replacement screen + battery and test touch, color, brightness, and sensors.\n"
                    "3. Disconnect battery, apply thin even adhesive bead, seat screen flush, and clamp 30–60 mins."
                ),
                "safety_and_traps": (
                    "TRAP: Leaving a tiny glass shard in the frame corner or clamping too hard on fragile OLED edges."
                ),
                "real_life_scenario": (
                    "A newly installed screen lifts on the right edge after two days because old adhesive "
                    "was not scraped clean and the frame was slightly bent."
                ),
                "practice_activity": (
                    "Write your 6-point pre-adhesive test checklist for a smartphone display replacement."
                ),
                "checkpoint_questions": (
                    "1. Why must all glass shards be removed from the frame channel before seating a new OLED?\n"
                    "2. Why test the replacement screen before applying frame adhesive?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=2,
            defaults={
                "title": "Step 4: Battery Removal, Charging Sub-Board Swap & USB-C Port Soldering",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Release glued batteries safely using pull tabs or controlled IPA softening.\n"
                    "- Replace charging sub-boards and solder USB-C ports cleanly."
                ),
                "why_it_matters": (
                    "Charging faults and worn batteries are the #1 repeat repair request in every mobile shop."
                ),
                "core_explanation": (
                    "Stretch factory pull-tabs slowly at a low angle; if a tab snaps, apply a few drops "
                    "of 99% IPA along the battery edge to soften adhesive and lift gently with a wide plastic "
                    "card. Verify microphone, loudspeaker, antenna coaxial cable, and fast-charging current "
                    "after replacing a charging sub-board."
                ),
                "step_by_step_field_guide": (
                    "1. Disconnect battery FPC and pull adhesive tabs slowly at a low horizontal angle.\n"
                    "2. Fit new battery with fresh adhesive strips and confirm snug fit.\n"
                    "3. Swap/repair charging sub-board, re-clip coaxial antenna wire cleanly, and verify fast charge + mic."
                ),
                "safety_and_traps": (
                    "TRAP: Forgetting to reconnect the thin coaxial antenna wire—leaving the client with 'No Service'."
                ),
                "real_life_scenario": (
                    "After a charging port replacement, the phone charges fast but has weak cellular signal "
                    "because the coaxial antenna cable was pinched under a screw boss."
                ),
                "practice_activity": (
                    "Document the post-repair test steps after replacing a phone charging sub-board."
                ),
                "checkpoint_questions": (
                    "1. What happens if the coaxial antenna cable is left disconnected or pinched?\n"
                    "2. How do you safely remove a battery if its stretch pull-tab breaks?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: Android/iOS Software Recovery, Bootloops & Firmware Flashing",
                "tier": "tier_2",
                "summary": "Resolve software bootloops, failed updates, and storage errors safely.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 5: Bootloop Triage, Recovery Mode & Stock Firmware Restoration",
                "estimated_minutes": 50,
                "learning_objectives": (
                    "- Distinguish software bootloops from stuck power buttons or failing batteries.\n"
                    "- Restore stock firmware safely using exact model/region identifiers."
                ),
                "why_it_matters": (
                    "Flashing wrong firmware variants permanently bricks phones, whereas accurate model "
                    "matching turns software crashes into fast, high-margin repairs."
                ),
                "core_explanation": (
                    "Before flashing, inspect physical power/volume buttons (a stuck volume key forces "
                    "Recovery/Fastboot loop) and test battery voltage. Verify exact model code, carrier/region, "
                    "and binary/bootloader version before flashing official firmware."
                ),
                "step_by_step_field_guide": (
                    "1. Rule out stuck buttons, low battery (<3.7V), or shorted flex cables.\n"
                    "2. Confirm exact device model/variant and warn client regarding data erasure.\n"
                    "3. Boot into Recovery/Download/DFU mode and flash verified stock firmware."
                ),
                "safety_and_traps": (
                    "TRAP: Flashing firmware from a different regional/hardware variant or letting battery "
                    "die mid-flash."
                ),
                "real_life_scenario": (
                    "A phone keeps rebooting into Recovery Mode—cleaning a sticky volume-up button fixes "
                    "it in 5 minutes without wiping user photos."
                ),
                "practice_activity": (
                    "List 3 hardware checks to perform before concluding a bootloop requires firmware flashing."
                ),
                "checkpoint_questions": (
                    "1. How can a stuck volume button mimic a software bootloop?\n"
                    "2. Why must firmware model/variant numbers match exactly?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Smartphone Component & Software Proficiency Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test screen/battery/charging-board replacement and firmware recovery mastery.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="After replacing a smartphone's charging sub-board, the phone charges normally, but the client reports 'No Service' or weak signal. What should you check first?",
            option_a="Whether the thin coaxial RF antenna cable was re-clipped properly and not pinched",
            option_b="Whether the screen brightness is at 100%",
            option_c="Whether the wallpaper color was changed",
            option_d="Whether the SIM tray is made of plastic",
            correct_answer="A",
            explanation="The coaxial antenna cable runs directly from the charging sub-board to the mainboard; if unclipped or pinched, cellular reception drops.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="Before flashing stock firmware onto a bootlooping phone, which physical check should you perform first?",
            option_a="Verify power/volume buttons are not stuck and battery voltage is sufficient",
            option_b="Heat the OLED screen to 150°C",
            option_c="Remove the camera lenses",
            option_d="Glue the back cover shut permanently",
            correct_answer="A",
            explanation="A stuck volume button forces boot-mode loops, and low battery voltage can interrupt flashing mid-way.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): BOARD-LEVEL DIAGNOSTICS, MICRO-SOLDERING & SHOP OPS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-3-professional",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 3: Board Fault-Finding, Micro-Soldering & Shop Operations",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Trace mobile power rails (VBAT, VPH_PWR), isolate "
                    "shorted SMD capacitors/ICs, perform shielded hot-air rework, manage repair shop "
                    "pricing/warranties, and qualify for QR-verifiable certification & transcript."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 14,
                "credential_awarded": "Tier 3 Master Smartphone Technician QR Certificate & Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus DC Bench Power Supply (current-limited), "
                    "Stereo Microscope, Hot-Air Rework Station, Micro-Soldering Pencil, Low-Melt Solder, "
                    "Kapton Tape, Board Schematics / Bitmap Viewer"
                ),
                "safety_guidelines": (
                    "1. CURRENT LIMITING: Limit DC bench power supply current when injecting voltage to find shorted mobile rails.\n"
                    "2. HEAT SHIELDING: Shield plastic FPC connectors, microphones, and underfilled ICs with Kapton/metal shields.\n"
                    "3. CUSTOMER PRIVACY & DATA ETHICS: Never browse customer photos, messages, or banking apps."
                ),
                "field_tips_summary": (
                    "Never quote a fixed 'cheap' price on water-damaged or dead-board phones before running "
                    "current-draw diagnostics—charge a clear diagnostic fee or tiered board-repair rate."
                ),
                "course_glossary_overview": (
                    "Covers VBAT / VPH_PWR Rails, Diode Mode Readings, Short-to-Ground, Underfill, "
                    "FPC Connector Rework, Tristar/Hydra/Charging IC, and Workshop Warranty/Intake SOP."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Mobile Logic-Board Power Rails, Short Isolation & Micro-Rework",
                "tier": "tier_3",
                "summary": "Diagnose dead/liquid-damaged boards and replace SMD connectors/components cleanly.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 6: DC Bench Power Analysis, Primary Rail Shorts & Liquid-Damage Recovery",
                "estimated_minutes": 70,
                "learning_objectives": (
                    "- Interpret DC bench power supply current draw (pre-boot vs. prompt-to-boot).\n"
                    "- Isolate shorted SMD filter capacitors and clean ultrasonic/IPA corrosion safely."
                ),
                "why_it_matters": (
                    "Many 'dead' water-damaged phones have a single shorted capacitor on the primary power "
                    "rail—finding and removing it restores the phone and preserves priceless user data."
                ),
                "core_explanation": (
                    "Connect the bare mainboard to a current-limited DC bench supply: high immediate current "
                    "before pressing power indicates a primary rail (VBAT/VPH_PWR) short; zero response on "
                    "power press points to power-button line or PMIC trigger issues."
                ),
                "step_by_step_field_guide": (
                    "1. Inspect bare board under microscope for green/white corrosion around connectors.\n"
                    "2. Check battery connector rails in diode/continuity mode for short to ground.\n"
                    "3. Use current-limited bench testing/thermal detection to pinpoint the shorted component.\n"
                    "4. Replace faulty component, clean flux/corrosion thoroughly, and verify boot current."
                ),
                "safety_and_traps": (
                    "TRAP: Scrubbing tiny SMD components off the board with stiff brushes or overheating underfilled CPUs."
                ),
                "real_life_scenario": (
                    "A dropped-in-water phone draws 1.2A immediately on DC bench connection before pressing "
                    "power; isolating one cracked filter capacitor clears the short."
                ),
                "practice_activity": (
                    "Write the diagnostic interpretation for: (a) 0.90A draw before power press, and "
                    "(b) 0.00A draw before and after pressing power."
                ),
                "checkpoint_questions": (
                    "1. What does immediate high current draw before pressing power indicate?\n"
                    "2. Why inspect corroded boards under magnification before applying power?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 7: Shielded FPC Connector Rework & Repair Shop Pricing / Warranty SOP",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Replace damaged FPC board connectors without melting plastic housings.\n"
                    "- Price mobile repairs profitably and enforce clear warranty and data-privacy policies."
                ),
                "why_it_matters": (
                    "Damaged display/battery FPC connectors are common after DIY repair attempts; mastering "
                    "clean rework and structured shop policies makes your workshop bankable."
                ),
                "core_explanation": (
                    "Protect adjacent plastics with Kapton tape, use low-melt alloy/controlled hot air to "
                    "remove crushed FPC sockets without lifting pads, solder the replacement cleanly, and "
                    "document clear warranty exclusions (drops, liquid, tampering) on every receipt."
                ),
                "step_by_step_field_guide": (
                    "1. Mask surrounding components with Kapton tape and apply flux.\n"
                    "2. Remove damaged FPC connector cleanly, wick pads flat, and seat new connector.\n"
                    "3. Inspect every pin under magnification and test display/touch/charging.\n"
                    "4. Issue itemized receipt with warranty duration and care guidelines."
                ),
                "safety_and_traps": (
                    "TRAP: Melting a new plastic FPC connector by blasting hot air directly from above instead "
                    "of controlled pre-heat/bottom or angled airflow."
                ),
                "real_life_scenario": (
                    "A phone arrives after an amateur tore pins off the display FPC socket; clean socket "
                    "replacement restores full display and touch."
                ),
                "practice_activity": (
                    "Draft a 1-page Mobile Repair Shop Intake, Pricing & Warranty Policy."
                ),
                "checkpoint_questions": (
                    "1. How do you prevent melting a new plastic FPC socket during soldering?\n"
                    "2. Why must repair receipts clearly state warranty exclusions?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Smartphone Board & Shop Operations Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Smartphone Technician QR Certificate & Transcript.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="When you connect a bare smartphone motherboard to a current-limited DC bench power supply, it immediately pulls 1.1A BEFORE you press the power button. What does this indicate?",
            option_a="A short circuit on a primary power rail (such as VBAT or VPH_PWR)",
            option_b="The wallpaper resolution is too high",
            option_c="The speaker volume is muted",
            option_d="The phone is fully charged and ready for pickup",
            correct_answer="A",
            explanation="Current draw before pressing the power trigger points to a leak or short on a primary always-on power rail.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="How do you protect adjacent plastic connectors and microphones when using hot air on a smartphone motherboard?",
            option_a="Mask nearby components with Kapton tape/heat shields and control temperature and airflow",
            option_b="Pour water over nearby connectors while heating",
            option_c="Set airflow and heat to maximum and hold in one spot",
            option_d="Leave the battery plugged in to absorb heat",
            correct_answer="A",
            explanation="Kapton tape/heat shields and controlled airflow prevent melting adjacent plastics or damaging MEMS microphones.",
        )

        # =====================================================================
        # GLOSSARY TERMS (AVAILABLE FROM TIER 1 & ACROSS ALL THREE TIERS)
        # =====================================================================
        glossary_items = [
            ("safety", "ESD", "Electrostatic Discharge", "Sudden static electricity discharge that can damage sensitive ICs.", "Wear an anti-static wrist strap/mat before handling exposed mobile boards.", True, 1),
            ("equipment", "LiPo Pouch", "Lithium-Polymer Pouch Battery", "Thin soft-foil rechargeable battery used in smartphones.", "Never pry with metal tools or puncture; risk of fire.", True, 2),
            ("equipment", "FPC", "Flexible Printed Circuit Connector", "Snap-on or ZIF ribbon connector linking displays, batteries, and cameras.", "Unclip battery FPC first and align carefully before pressing down.", True, 3),
            ("equipment", "OLED / AMOLED", "Organic Light-Emitting Diode Display", "Thin self-lit smartphone display panel.", "Test loosely before gluing and clean frame glass shards completely.", True, 4),
            ("general", "Bootloop", "Repeated Startup Restart Cycle", "Device restarts continuously without reaching the home screen.", "Check stuck buttons and battery voltage before flashing stock firmware.", False, 5),
            ("equipment", "VBAT / VPH_PWR", "Main Battery / Primary System Power Rail", "Always-on primary voltage rails feeding smartphone power circuits.", "Immediate current draw on DC bench supply points to a primary rail short.", False, 6),
            ("tools", "Kapton Tape", "Polyimide High-Temperature Masking Tape", "Heat-resistant insulating tape used during hot-air rework.", "Protects nearby plastic sockets and SMD parts from heat.", False, 7),
        ]

        for group, term, expansion, definition, application, tier1_flag, order in glossary_items:
            for target_course in (tier1_course, tier2_course, tier3_course):
                TradeGlossaryTerm.objects.update_or_create(
                    course=target_course,
                    term=term,
                    defaults={
                        "category": category,
                        "topic_group": group,
                        "full_expansion": expansion,
                        "definition": definition,
                        "field_application": application,
                        "available_from_tier_1": tier1_flag,
                        "order": order,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded Smartphone Hardware & Software Repair across Tier 1, Tier 2, and Tier 3, "
                "including lessons, glossary terms, and quizzes!"
            )
        )