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
    help = (
        "Seeds the complete 3-tier Smartphone Hardware & Software Repair course, "
        "diagrams, reference tables, glossary, and assessments."
    )

    def handle(self, *args, **options):
        target_name = "Smartphone Hardware & Software Repair"
        target_description = (
            "Practical smartphone diagnostics, pre/post-repair intake testing, safe battery and "
            "display replacement, charging/audio/camera/board-level troubleshooting, software "
            "recovery, and ethical repair shop operations."
        )

        category, _ = TradeCategory.objects.update_or_create(
            slug="smartphone-repair",
            defaults={
                "name": target_name,
                "description": target_description,
            },
        )
        if hasattr(category, "name_en"):
            category.name_en = target_name
        if hasattr(category, "description_en"):
            category.description_en = target_description
        if hasattr(category, "name_en") or hasattr(category, "description_en"):
            category.save()

        # =====================================================================
        # TIER 1 (FREE): FOUNDATION, INTAKE TRIAGE & BENCH SAFETY
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 1: Bench Safety, Intake Triage & Core Terminology",
                "description": (
                    "FREE TIER: Build sound repair habits with ESD & lithium-ion battery safety, "
                    "essential technician tools, structured intake testing, customer data-privacy awareness, "
                    "and core mobile repair terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Mobile Bench Readiness Record",
                "required_tools": (
                    "ESD-Safe Mat & Wrist Strap, Precision Driver Set (Phillips, Torx, Tri-point, Pentalobe), "
                    "Plastic Pry Tools & Spudgers, Tweezers, USB Power/Amp Meter, Magnifier/Lamp, "
                    "Intake Checklist & Sand/Fireproof Containment Bucket"
                ),
                "safety_guidelines": (
                    "1. Ground yourself with an ESD strap on a grounded mat before handling exposed logic boards or flex cables.\n"
                    "2. Never puncture, bend, crush, or apply high heat directly to lithium-ion batteries.\n"
                    "3. Keep a non-flammable containment bucket/sand nearby and log pre-existing damage/data risks before opening."
                ),
                "field_tips_summary": (
                    "Always test every function on intake before touching a screw, never use metal pry tools "
                    "near batteries or flex connectors, and get clear customer sign-off on data and pre-existing faults."
                ),
                "course_glossary_overview": (
                    "Covers ESD, Li-Ion, LCD vs. OLED/AMOLED, FPC, IMEI, FRP, DFU/Recovery, "
                    "and USB VBUS/Amp draw so technicians read specs and customer faults accurately."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Bench Safety, Intake Diagnostics & Mobile Terminology",
                "tier": "tier_1",
                "summary": "Safe workbench setup, pre-repair intake testing, data/liability habits, and starter terms.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: Workbench Setup, ESD Protection, Lithium Safety & Intake Triage",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Set up a safe, organized repair bench with ESD protection and lithium-ion hazard controls.\n"
                    "- Run a structured pre-repair intake check covering power, display, touch, cameras, audio, mics, sensors, and charging.\n"
                    "- Protect customer privacy, backups, and shop liability before opening any device."
                ),
                "why_it_matters": (
                    "A single static discharge or punctured battery can ruin a board or cause a bench fire, "
                    "while skipping an intake check leads to blaming your repair for a Face ID, fingerprint, "
                    "camera, or speaker fault that already existed before the phone arrived."
                ),
                "core_explanation": (
                    "PRE-REPAIR INTAKE & SAFETY MATRIX:\n"
                    "- ESD Control: Static electricity can damage sensitive ICs without a visible spark; wear a grounded ESD wrist strap on an ESD mat and keep synthetic/fleece clothing clear of exposed boards.\n"
                    "- Lithium-Ion Battery Care: Swollen, dented, or punctured cells can vent gas or catch fire; use plastic spudgers, controlled gentle warming (never hot-air blasting a swollen cell), and keep a sand/fire-safe bin ready.\n"
                    "- Baseline Intake Test: Before disassembly, inspect frame bends/cracks/liquid indicators and test display uniformity, touch across all zones, earpiece/loudspeaker, mics, cameras, charging port/USB current, Wi-Fi/Bluetooth, and biometric/sensor behavior.\n"
                    "- Customer & Data Care: Advise backups before software/hardware work, log existing faults on the intake ticket, and treat customer photos/messages/accounts strictly confidentially.\n\n"
                    "INTAKE TRIAGE CHECKLIST:\n"
                    "Stage        | What to Record Before Teardown\n"
                    "-------------+-------------------------------------------------------------\n"
                    "Housing/LDI  | Dents, frame warp, back glass cracks, liquid indicator state\n"
                    "Core I/O     | Touch grid, display spots/lines, mic/speaker, cameras, USB A\n"
                    "Data & Lock  | Backup warning given, account lock status, client sign-off"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Clear clutter, lay down the ESD mat, connect wrist strap, and verify containment bin is within reach.\n\n"
                    "INTAKE & SAFETY STEPS:\n"
                    "1. Inspect the exterior housing for dents, frame distortion, back-glass cracks, or moisture signs and log them on the intake form.\n"
                    "2. Test core functions (display, touch grid, speakers, mics, cameras, buttons, SIM/network, charging current) and record any pre-existing failures.\n"
                    "3. Remind the client about data backup risks and obtain clear repair authorization.\n"
                    "4. Power down or isolate safely, sort screws by length/position in a magnetic/compartment mat, and never pry near the battery with sharp metal.\n\n"
                    "POST-INTAKE CHECK:\n"
                    "- Confirm every screw, shield, and pre-existing fault is documented before starting teardown."
                ),
                "safety_and_traps": (
                    "- TRAP (Blaming the Tech for Pre-Existing Faults): If a front camera, proximity sensor, or fingerprint reader was already dead and you didn't record it at intake, the client may hold you responsible after the repair.\n"
                    "- TRAP (Prying/Levering Lithium Batteries): Metal screwdrivers or sharp blades can puncture a pouch cell or slice an underlying display/board flex cable.\n"
                    "- TRAP (Mixing Tiny Screws of Different Lengths): Driving a long screw into a short-screw hole can pierce the logic board layers beneath."
                ),
                "diagram_or_visual_guide": (
                    "[Client Device Arrives] ---> [Log Frame/Liquid/Existing Faults + Data Notice]\n"
                    "                       ---> [ESD Mat & Strap + Plastic Tools Only]\n"
                    "                       ---> [Safe Teardown & Screw Mapping]"
                ),
                "real_life_scenario": (
                    "A customer brings in a phone with a cracked screen. You test it at intake and note that the "
                    "earpiece speaker is quiet and the rear camera autofocus is sluggish, then write both on the intake "
                    "slip. After replacing the screen, the customer asks why the camera still struggles—your intake record "
                    "and calm explanation prevent a dispute and let you quote the camera module transparently."
                ),
                "practice_activity": (
                    "Perform a 15-minute intake audit on a smartphone: check exterior housing/buttons/ports, test "
                    "touch/display/audio/cameras/charging, and write a clean intake summary listing any faults and data advice."
                ),
                "checkpoint_questions": (
                    "1. Why must you test and log device functions BEFORE starting a repair?\n"
                    "2. Why should you avoid metal pry tools and high concentrated heat on a lithium-ion battery?\n"
                    "3. Why does screw length/position matter on modern smartphones?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Core Mobile Hardware, Software & Diagnostic Terminology",
                "estimated_minutes": 40,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Define key mobile hardware, display, charging, and software terms accurately.\n"
                    "- Distinguish symptoms from root causes when talking to customers and parts suppliers."
                ),
                "why_it_matters": (
                    "Ordering the wrong screen type, charging flex, or diagnostic mode wastes money and time. "
                    "Clear terminology helps you diagnose accurately and explain repairs simply to clients."
                ),
                "core_explanation": (
                    "ESSENTIAL MOBILE REPAIR TERMS:\n"
                    "- ESD (Electrostatic Discharge): Sudden static transfer that can weaken or destroy sensitive semiconductors.\n"
                    "- FPC (Flexible Printed Circuit): Thin ribbon cable/connector carrying signals or power between modules and the logic board.\n"
                    "- LCD vs. OLED / AMOLED: LCD uses a backlight layer behind liquid crystals; OLED/AMOLED pixels emit their own light (deeper blacks, higher contrast, often thinner and more impact/pressure sensitive).\n"
                    "- USB VBUS / Amp Draw: Charging supply voltage (~5V standard or higher fast-charge negotiation) and current draw (Amps) measured with a USB tester.\n"
                    "- IMEI: Unique 15-digit device identifier used for network/device tracking and verification.\n"
                    "- FRP / Activation Lock: Security lock tying a reset device to a prior Google/Apple account—requires legitimate owner credentials.\n"
                    "- Recovery / Fastboot / DFU Mode: Low-level boot states used for legitimate diagnostics, updates, or firmware flashing.\n\n"
                    "DISPLAY & DIAGNOSTIC COMPARISON:\n"
                    "Term / Aspect   | Key Technical Meaning\n"
                    "----------------+-------------------------------------------------------------\n"
                    "LCD vs. OLED    | Backlit liquid crystal vs. self-emissive pixels\n"
                    "FPC & USB Amp   | Ribbon interconnect vs. measured charging current (A)\n"
                    "IMEI / FRP / DFU| Device ID, owner account lock, low-level boot/flash mode"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Verify exact model number and build/region details before ordering replacement parts or firmware files.\n\n"
                    "TERMINOLOGY & SPEC CHECK STEPS:\n"
                    "1. Confirm exact device model/variant—not just marketing name—before buying screens, batteries, or charging boards.\n"
                    "2. Check whether the original display is LCD or OLED/AMOLED so you quote accurate part quality and handle glass/flex carefully.\n"
                    "3. Use a USB power/amp meter to observe charging negotiation and current draw rather than guessing from a blinking icon.\n"
                    "4. Check software/account status ethically before promising a software reset or flash.\n\n"
                    "POST-CHECK:\n"
                    "- Record exact part type, test readings, and software version on the job ticket."
                ),
                "safety_and_traps": (
                    "- TRAP (Assuming Same Model Name = Same Part): Regional or carrier sub-models can have different batteries, flex cables, or antennas.\n"
                    "- TRAP (Promising Software Fixes That Bypass Account Locks): Never promise unlocking/bypassing owner security locks without authorized ownership proof and legal compliance.\n"
                    "- TRAP (Trusting a Blinking Charging Icon): A phone can display a charging graphic while drawing near-zero current due to a worn cable, dirty port, or faulty charge circuit."
                ),
                "diagram_or_visual_guide": (
                    "[Exact Model ID] ---> [Display Type (LCD/OLED) + Part Spec]\n"
                    "                 ---> [USB Tester (V / A Draw)]\n"
                    "                 ---> [Software State (Boot/Recovery/Account)]"
                ),
                "real_life_scenario": (
                    "A client says 'my phone won't charge.' Plugging in a USB amp meter shows 5.0V at 0.02A—the icon "
                    "appears briefly, but real charging current isn't flowing. Checking the charging port lint, cable, "
                    "and battery/charging path pinpoints the real issue instead of guessing."
                ),
                "practice_activity": (
                    "Write clear definitions and one practical repair example for: FPC, OLED vs. LCD, USB Amp Draw, IMEI, and FRP."
                ),
                "checkpoint_questions": (
                    "1. What is the practical difference between LCD and OLED/AMOLED displays during handling and replacement?\n"
                    "2. Why is a USB power/amp meter more informative than watching the screen charging icon alone?\n"
                    "3. Why must you verify the exact sub-model before ordering replacement components?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Mobile Bench Safety & Intake Triage Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify your grasp of bench safety, intake testing, and core mobile repair terms.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="A customer brings in a phone with a shattered screen. What should you do BEFORE starting disassembly?",
            option_a="Immediately pry the battery out with a metal screwdriver",
            option_b="Perform a pre-repair intake check, log existing faults/damage, and advise on data/backups",
            option_c="Skip testing cameras and speakers since only the screen looks broken",
            option_d="Apply high direct heat to the battery cell until it pops loose",
            correct_answer="B",
            explanation="Testing and logging existing conditions at intake protects against false blame, and data/safety checks prevent avoidable loss or injury.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="Which component is a thin flexible ribbon/connector carrying signals or power inside a smartphone?",
            option_a="FPC (Flexible Printed Circuit)",
            option_b="IMEI",
            option_c="FRP",
            option_d="Sand bucket",
            correct_answer="A",
            explanation="An FPC (Flexible Printed Circuit) is the flexible ribbon/connector assembly used inside mobile devices.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): DISPLAY, BATTERY, CHARGING & SOFTWARE RECOVERY
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 2: Displays, Batteries, Charging & Software",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Safely open housings, replace displays and batteries, "
                    "service charging ports/sub-boards, perform software diagnostics & firmware recovery, "
                    "and run full post-repair quality verification."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 12,
                "credential_awarded": "Tier 2 Practical Mobile Technician Certificate & Interim Transcript",
                "required_tools": (
                    "All Tier 1 tools plus Controlled Heat Pad / Hot Air Station, Isopropyl Alcohol (IPA) & "
                    "Safe Adhesive/Pull-Tab Solvent, Suction Cup & Thin Pry Cards, Regulated DC Power Supply "
                    "(for bench checks), Adhesive Frames & Seal Strips"
                ),
                "safety_guidelines": (
                    "1. Disconnect or isolate the battery flex/circuit early and never short battery contacts.\n"
                    "2. Use controlled, even heat (avoiding overheating batteries or OLED layers) and plastic cards—never force stuck parts.\n"
                    "3. Test new displays and batteries before final adhesive sealing and verify all functions post-repair."
                ),
                "field_tips_summary": (
                    "Always test a replacement screen/battery before sealing permanently, clean old adhesive "
                    "cleanly so frames sit flush, and verify every sensor and call/audio path before handover."
                ),
                "course_glossary_overview": (
                    "Covers adhesive softening, OLED pressure/burn-in care, battery health/cycle checks, "
                    "charging port/FPC diagnostics, firmware recovery, and post-repair QA checklists."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: Safe Teardown, Display Replacement & Battery Servicing",
                "tier": "tier_2",
                "summary": "Open devices cleanly, replace screens and batteries safely, and avoid display/cell damage.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: Safe Device Opening, Display Assembly Replacement & Pre-Seal Testing",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Soften adhesives safely and separate back covers or display assemblies without tearing flex cables.\n"
                    "- Transfer proximity/ambient/speaker/biometric components cleanly where required.\n"
                    "- Test display image, brightness, touch responsiveness, and sensors before applying final adhesive."
                ),
                "why_it_matters": (
                    "Tearing a display or earpiece flex during opening—or sealing a defective screen with strong "
                    "adhesive before testing—turns a profitable repair into an expensive loss."
                ),
                "core_explanation": (
                    "DISPLAY REPLACEMENT & PRE-SEAL TEST RULES:\n"
                    "- Controlled Separation: Warm adhesive edges evenly at safe temperatures, use thin flexible cards/picks, and slide gently without gouging deep under delicate flex ribbons.\n"
                    "- Flex & Shield Care: Remove battery connection/shielding carefully, release FPC latches properly (flip-up or straight-pull per connector design), and never yank a ribbon cable.\n"
                    "- Test Before Final Glue: Connect the replacement display assembly (and battery), power on briefly, and test touch across the entire screen, brightness control, true-tone/auto-brightness, and call/proximity behavior before permanent bonding.\n\n"
                    "DISPLAY & SEAL QUALITY CHECKS:\n"
                    "Check Stage   | What to Confirm\n"
                    "--------------+-------------------------------------------------------------\n"
                    "Frame Prep    | Old glue & glass shards cleared so frame sits completely flat\n"
                    "Pre-Seal Test | Full touch grid, brightness, cameras, ear/loudspeaker & sensors\n"
                    "Final Closure | Even adhesive/clamp pressure; zero light bleed or gaps"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Power off the device, remove SIM tray, and confirm ESD strap connection.\n\n"
                    "DISPLAY REPLACEMENT STEPS:\n"
                    "1. Apply gentle, even heat along the perimeter seam; create a small gap with a suction cup/thin pick and work around the perimeter using plastic shims.\n"
                    "2. Open carefully like a book or hinge—watch for attached flex cables before lifting completely.\n"
                    "3. Disconnect battery and display FPCs, remove broken assembly, clean old adhesive debris from the frame, and transfer needed small parts.\n"
                    "4. Connect the new display and battery temporarily, power on, and run a full touch/display/sensor check BEFORE final sealing.\n\n"
                    "POST-REPAIR CHECK:\n"
                    "- Clean adhesive evenly, seat frame flush with even clamping pressure, and re-test touch, cameras, and audio."
                ),
                "safety_and_traps": (
                    "- TRAP (Prying Deep Near the Hinge/Flex): Thin display and sensor flexes sit right near frame edges—keep pry depth shallow and controlled.\n"
                    "- TRAP (Gluing Before Testing): Permanent adhesive makes returns hard and risks cracking a new screen during removal.\n"
                    "- TRAP (Leftover Glass/Adhesive Chunks): A tiny shard or lump of old glue under a new OLED panel can cause pressure spots or cracks when pressed."
                ),
                "diagram_or_visual_guide": (
                    "[Gentle Edge Heat + Thin Shim] ---> [Open Carefully & Watch Flexes]\n"
                    "                              ---> [Clean Frame + Temporary Bench Test]\n"
                    "                              ---> [Final Seal + Full QA Check]"
                ),
                "real_life_scenario": (
                    "You install a replacement screen and seal it right away, only to notice a dead touch strip on "
                    "one edge afterward. Testing the display temporarily with a light hold before final adhesive sealing "
                    "lets you catch faulty parts immediately and save rework."
                ),
                "practice_activity": (
                    "Write out your step-by-step display replacement and pre-seal test checklist, including two mistakes "
                    "that cause touch or display failure right after installation."
                ),
                "checkpoint_questions": (
                    "1. Why should you test a replacement display before applying final adhesive?\n"
                    "2. How do old glue or glass fragments affect a new display when pressed into the frame?\n"
                    "3. Why must you check flex cable orientation before lifting an opened cover?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=2,
            defaults={
                "title": "Step 4: Battery Diagnostics, Safe Removal & Replacement",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Identify signs of battery wear, swelling, or voltage/health degradation.\n"
                    "- Remove glued or pull-tab batteries safely without puncturing or bending the cell.\n"
                    "- Install a verified replacement battery and confirm stable charging and runtime."
                ),
                "why_it_matters": (
                    "Batteries carry real thermal and chemical risk if mishandled, while low-quality or poorly "
                    "seated batteries cause sudden shutdowns, rapid drain, or screen push-out."
                ),
                "core_explanation": (
                    "BATTERY SERVICE STANDARDS:\n"
                    "- When to Replace: Rapid percentage drop, sudden shutdowns under load, poor battery health/capacity, or physical swelling.\n"
                    "- Safe Removal: Pull stretch-release tabs smoothly at a low angle without snapping them; if adhesive is stiff, use minimal safe solvent/heat—never lever forcefully against the logic board or flex cables.\n"
                    "- Swollen Battery Rule: Treat swollen batteries with extra caution—do not squeeze or puncture them, and dispose/handle them safely according to local hazardous/e-waste rules."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Power off the device, wear eye protection and ESD gear, and keep a fire-safe containment bin nearby.\n\n"
                    "BATTERY REPLACEMENT STEPS:\n"
                    "1. Disconnect the battery connector and any covering bracket carefully.\n"
                    "2. Release pull-tabs slowly at a low angle or gently soften adhesive without overheating the cell.\n"
                    "3. Lift the old battery out evenly without bending it, inspect the compartment for debris or swelling residue, and seat the new battery cleanly.\n"
                    "4. Reconnect the battery and shields, then test power-on, charging current, and basic device operation.\n\n"
                    "POST-REPAIR CHECK:\n"
                    "- Verify the battery sits flat without pushing the back cover or screen, and log health/charging readings."
                ),
                "safety_and_traps": (
                    "- TRAP (Snapping Pull Tabs): Pulling fast or at a steep angle snaps stretch-release strips, leaving strong glue underneath.\n"
                    "- TRAP (Using Metal Knives/Screwdrivers as Levers): Piercing a lithium cell can cause smoking, fire, or chemical burns.\n"
                    "- TRAP (Ignoring Swelling): A swollen battery can push up and crack a display if forced shut."
                ),
                "diagram_or_visual_guide": (
                    "[Isolate Battery] ---> [Careful Tab/Adhesive Release] ---> [Inspect Compartment]\n"
                    "                 ---> [Seat New Battery Flat] ---> [Verify Charge & Stability]"
                ),
                "real_life_scenario": (
                    "A client's phone shuts off at 35% battery and the back cover feels slightly raised. Inspecting "
                    "reveals mild battery swelling. You safely remove the worn cell without prying with sharp metal, "
                    "fit a quality replacement battery, verify charging current, and arrange proper disposal of the old cell."
                ),
                "practice_activity": (
                    "List the safety precautions and step-by-step checks you perform before and after replacing a smartphone battery."
                ),
                "checkpoint_questions": (
                    "1. What signs indicate a smartphone battery needs replacement?\n"
                    "2. What happens if you pull battery adhesive tabs too fast or at a sharp angle?\n"
                    "3. Why is inspecting the battery compartment for flatness important before closing the phone?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: Charging / Peripheral Modules & Software Diagnostics",
                "tier": "tier_2",
                "summary": "Troubleshoot charging/audio/camera modules and run safe software recovery & diagnostics.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 5: Charging Ports, Sub-Boards, Audio/Camera Flexes & Modular Swaps",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Diagnose slow or non-charging ports, loose charging sub-boards, and faulty camera/audio modules.\n"
                    "- Clean ports safely and replace modular flex/sub-board assemblies cleanly.\n"
                    "- Confirm charging current, microphone/speaker clarity, and camera focus after repair."
                ),
                "why_it_matters": (
                    "Many 'dead phone' or 'broken charging' complaints come down to lint in the USB port, a loose "
                    "FPC, or a faulty sub-board—easy to fix cleanly when diagnosed systematically."
                ),
                "core_explanation": (
                    "MODULAR HARDWARE DIAGNOSTICS:\n"
                    "- Charging Faults: Check cable and charger first, inspect USB port for compacted lint/debris/bent pins, test with a USB amp meter, and check charging sub-board/flex connections.\n"
                    "- Camera & Audio Modules: Muffled audio or blurry/non-focusing cameras often trace to clogged speaker meshes, loose FPC connectors, or damaged camera/mic modules.\n"
                    "- Modular Replacement: Swap complete sub-boards or camera/speaker flex modules when damaged rather than guessing.\n\n"
                    "MODULAR FAULT-TO-CHECK MATRIX:\n"
                    "Complaint            | First Checks Before Replacing Board\n"
                    "---------------------+-------------------------------------------------------------\n"
                    "Slow / No Charging   | Known-good cable/charger, USB port lint/pins, USB amp meter\n"
                    "Muffled / No Audio   | Speaker grille dust/debris, audio/sub-board flex seating\n"
                    "Camera Blur / Error  | Lens/glass cleanliness, camera FPC latch & module seating"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Test with a known-good cable/adapter and USB meter before opening the device.\n\n"
                    "MODULAR SERVICE STEPS:\n"
                    "1. Inspect the charging port under magnification for debris or bent pins; clear gently with non-conductive tools.\n"
                    "2. Open safely, disconnect battery, and inspect relevant FPC connectors and sub-board seating.\n"
                    "3. Replace the faulty charging sub-board, speaker, mic, or camera module and re-seat connectors cleanly.\n"
                    "4. Reconnect battery and test charging current, voice recording/playback, and front/rear camera focus/flash.\n\n"
                    "POST-REPAIR CHECK:\n"
                    "- Confirm cable clicks firmly into the port and charging current stabilizes cleanly."
                ),
                "safety_and_traps": (
                    "- TRAP (Digging Metal Needles Inside USB Ports): Gouging inside a charging port with steel pins can bend/short power pins or scratch the port barrel.\n"
                    "- TRAP (Forcing Misaligned FPC Connectors): Align the connector key/notch first and press evenly—forcing an angled FPC bends pins."
                ),
                "diagram_or_visual_guide": (
                    "[USB Meter + Cable Check] ---> [Clean Port / Inspect Pins]\n"
                    "                         ---> [Check Sub-Board / Camera / Audio FPC]\n"
                    "                         ---> [Swap Faulty Module + Full I/O Test]"
                ),
                "real_life_scenario": (
                    "A customer's phone barely charges and the cable falls out easily. Inspecting the USB port under "
                    "magnification reveals tightly packed pocket lint at the back of the socket—careful cleaning restores "
                    "a firm plug fit and normal fast charging without opening the phone."
                ),
                "practice_activity": (
                    "Create a troubleshooting flow for a phone that charges intermittently and has muffled loudspeaker sound."
                ),
                "checkpoint_questions": (
                    "1. What simple check should you do first on a loose or slow-charging USB port?\n"
                    "2. Why align an FPC connector carefully before pressing it down?\n"
                    "3. How do you verify a speaker, mic, and camera repair before handover?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=2,
            defaults={
                "title": "Step 6: Software Diagnostics, OS Recovery, Flashing & Ethical Account/Data Care",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Distinguish software boot/app/storage issues from hardware faults.\n"
                    "- Execute safe forced restarts, cache/app troubleshooting, or official firmware recovery when authorized.\n"
                    "- Follow strict data-backup warnings and legal account/ownership rules."
                ),
                "why_it_matters": (
                    "A reset or firmware flash can erase irreplaceable photos or chats if the customer wasn't warned, "
                    "and unauthorized lock bypasses create serious legal and ethical liability."
                ),
                "core_explanation": (
                    "SOFTWARE RECOVERY & ETHICS:\n"
                    "- Safe Triage First: Check storage space, stuck background apps, corrupted updates, and forced-restart behavior before wiping data.\n"
                    "- Data & Ownership Discipline: Always explain that resets/re-flashes can wipe user data unless backed up, and verify legitimate ownership/credentials rather than assisting with unauthorized lock circumvention.\n\n"
                    "SOFTWARE ESCALATION LADDER:\n"
                    "Level 1 | Force restart, check storage & test in safe/diagnostic state\n"
                    "Level 2 | Targeted app/update fix without data loss where possible\n"
                    "Level 3 | Official recovery/re-flash (after backup warning & ownership check)"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Confirm battery charge level or stable power before starting any update/flash process.\n\n"
                    "SOFTWARE STEPS:\n"
                    "1. Record exact symptom, OS build/version, and storage/battery status.\n"
                    "2. Warn the customer about data-loss risk and confirm backup status before any reset or firmware flash.\n"
                    "3. Use verified firmware/tools matching the exact model/region and keep power steady throughout recovery.\n"
                    "4. Verify boot, Wi-Fi/cellular, camera, audio, and touch after recovery completes.\n\n"
                    "POST-RECOVERY CHECK:\n"
                    "- Document the software action taken and ensure customer accounts/privacy are respected."
                ),
                "safety_and_traps": (
                    "- TRAP (Wiping Data Without Warning): Factory-resetting or flashing a client's phone without warning about data loss destroys trust.\n"
                    "- TRAP (Flashing Wrong Firmware/Region or Losing Power Mid-Flash): Can brick or soft-lock a device.\n"
                    "- TRAP (Bypassing Account Locks Without Legitimate Proof): Creates legal, ethical, and security risks."
                ),
                "diagram_or_visual_guide": (
                    "[Symptom + Storage/Battery Check] ---> [Safe Triage / Force Restart]\n"
                    "                                    ---> [Backup Warning + Ownership Check]\n"
                    "                                    ---> [Official Recovery + Post-Boot Test]"
                ),
                "real_life_scenario": (
                    "A phone is stuck on the logo screen after an interrupted update. You explain that recovery may "
                    "reset data if unbacked up, apply the matching official recovery package with steady power, and "
                    "verify normal boot and connectivity before returning it."
                ),
                "practice_activity": (
                    "Write a short customer-facing explanation of why data backup matters before a software reset or re-flash."
                ),
                "checkpoint_questions": (
                    "1. Why should you warn a customer about data loss before performing a factory reset or firmware flash?\n"
                    "2. Why must firmware match the exact device model/variant?\n"
                    "3. Why is stable power critical during firmware recovery?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Practical Display, Battery, Charging & Software Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test your practical screen, battery, charging/modular, and software recovery judgment.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="You have fitted a replacement screen assembly on a phone. What is the smartest step BEFORE applying permanent adhesive and clamping it shut?",
            option_a="Test display image, touch across the whole screen, brightness, and key sensors/functions first",
            option_b="Glue it permanently immediately and skip testing",
            option_c="Leave leftover glass shards inside the frame to save cleaning time",
            option_d="Yank the display flex cable to test its tensile strength",
            correct_answer="A",
            explanation="Testing before final adhesive sealing catches faulty parts early and avoids costly rework.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="Why should you use plastic prying tools and controlled heat rather than sharp metal blades when removing a glued smartphone battery?",
            option_a="Sharp metal tools can puncture or short lithium-ion cells, creating fire or chemical hazards",
            option_b="Metal knives make batteries charge twice as fast",
            option_c="Plastic tools cannot lift any cover",
            option_d="Batteries are immune to punctures",
            correct_answer="A",
            explanation="Puncturing or shorting a lithium-ion battery can trigger overheating, venting, or fire.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): BOARD/LIQUID DIAGNOSTICS & SHOP / IOM READINESS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="smartphone-repair-tier-3-professional",
            defaults={
                "category": category,
                "title": "Smartphone Repair — Tier 3: Liquid/Board Diagnostics & Shop / Partner Mastery",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Triage liquid damage & board/power faults safely; quote "
                    "repairs transparently; manage parts/warranty boundaries; and build a trustworthy, "
                    "sustainable repair business or livelihood enterprise for QR certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 10,
                "credential_awarded": "Tier 3 Master Smartphone Repair Specialist QR Certificate & Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus Digital Multimeter, Microscope / Magnifier Lamp, "
                    "High-Purity Isopropyl Alcohol (IPA) & Ultrasonic/Brush Cleaning Kit, "
                    "Job Log, Transparent Quote Sheet & Warranty Slip"
                ),
                "safety_guidelines": (
                    "1. Disconnect power/battery immediately on liquid-damaged devices—never keep charging a wet/shorted phone.\n"
                    "2. Work methodically from symptom -> power/rail/module check -> root cause; never guess or apply reckless heat.\n"
                    "3. Give honest assessments when board/liquid damage has high uncertainty—never promise miracles on severely corroded boards."
                ),
                "field_tips_summary": (
                    "Honesty builds lifelong customers: tell clients upfront when liquid damage or severe board "
                    "faults carry risk, quote parts + labor clearly, and honor clear, fair warranty terms."
                ),
                "course_glossary_overview": (
                    "Covers Liquid Damage Triage, Corrosion/Short Isolation, Diagnostic Fee vs. Repair Quote, "
                    "Part Grade Tiers, Warranty Scope, and Customer/Partner Handover Records."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Liquid/Board Fault Isolation & Professional Shop Operations",
                "tier": "tier_3",
                "summary": "Handle liquid/board faults safely and run transparent quotes, warranties, and handover QA.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 7: Liquid Damage Triage, Corrosion Cleaning & Systematic Fault Isolation",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Take immediate safe steps when a phone is exposed to liquid or moisture.\n"
                    "- Inspect for corrosion/shorting and isolate whether a fault is modular, battery/charging, or board-level.\n"
                    "- Communicate realistic outcomes and risks clearly to the customer."
                ),
                "why_it_matters": (
                    "Plugging in a wet phone or powering a corroded board without inspection can cause short-circuit "
                    "damage, while honest expectations protect your shop from disputes over unpredictable liquid faults."
                ),
                "core_explanation": (
                    "LIQUID & BOARD FAULT ISOLATION:\n"
                    "- Immediate Containment: Power off if on, unplug chargers/accessories immediately, avoid putting wet phones in rice (which leaves dust/starch debris), and disconnect the battery as soon as safely opened.\n"
                    "- Inspection & Cleaning: Check liquid indicators and board/connector areas for moisture or corrosion residue; clean gently with high-purity IPA and soft brushes, allowing thorough drying before testing.\n"
                    "- Honest Risk Framing: Liquid and board faults can affect multiple circuits over time—explain findings and realistic success/risk upfront.\n\n"
                    "LIQUID & FAULT RESPONSE GUIDE:\n"
                    "Situation            | Safe / Practical Action\n"
                    "---------------------+-------------------------------------------------------------\n"
                    "Fresh Liquid Spill   | Power off, unplug charger, avoid rice dust, inspect/clean\n"
                    "Corrosion / Residue  | Disconnect battery, clean gently with IPA, dry thoroughly\n"
                    "Uncertain Board Fault| Isolate modules first; state realistic risk & quote clearly"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Ensure the device is unplugged and handled on an ESD-safe mat with proper ventilation.\n\n"
                    "LIQUID & FAULT STEPS:\n"
                    "1. Record liquid exposure details (water, drink, rain, salt/sea water) and set honest expectations with the client.\n"
                    "2. Open carefully, disconnect battery, and inspect connectors, shields, and visible board areas for moisture or corrosion.\n"
                    "3. Clean corrosion/residue carefully with IPA and soft non-metallic brushes, then allow complete drying.\n"
                    "4. Test with known-good modules/power checks and log results before deciding on further repair or return.\n\n"
                    "POST-CHECK:\n"
                    "- Never leave damp residue or unverified shorts powered unattended."
                ),
                "safety_and_traps": (
                    "- TRAP (Charging a Wet Phone): Applying power while liquid or corrosion bridges contacts can cause short circuits and burn traces.\n"
                    "- TRAP (Using Rice): Rice dust/starch can enter ports, speakers, and connectors without properly cleaning corrosion.\n"
                    "- TRAP (Guaranteeing Liquid/Board Recoveries): Corrosion can spread or affect hidden layers—always state risk transparently."
                ),
                "diagram_or_visual_guide": (
                    "[Liquid / Fault Reported] ---> [Unplug & Power Off / Isolate Battery]\n"
                    "                          ---> [Inspect & Clean Corrosion (IPA) + Dry]\n"
                    "                          ---> [Isolate Module vs. Board + Honest Quote]"
                ),
                "real_life_scenario": (
                    "A client drops a phone in water and tries charging it right away, causing it to turn off. You "
                    "unplug it immediately, open safely, disconnect the battery, clean visible corrosion around the "
                    "connector with IPA, dry thoroughly, and explain both what works and what risks remain."
                ),
                "practice_activity": (
                    "Write a 5-step response guide for a customer who just dropped their smartphone in water."
                ),
                "checkpoint_questions": (
                    "1. Why should you avoid plugging a liquid-damaged phone into a charger?\n"
                    "2. Why is putting a wet phone in rice a poor repair practice?\n"
                    "3. Why explain uncertainty clearly on liquid or board-level faults?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 8: Transparent Quoting, Warranty Boundaries & Sustainable Shop / Partner Operations",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Quote parts, diagnostic/labor time, and quality options clearly before starting paid work.\n"
                    "- Define clear, fair warranty boundaries (what is covered vs. excluded like new drops/liquid/wear).\n"
                    "- Maintain organized records that support repeat business and institutional/livelihood partnerships."
                ),
                "why_it_matters": (
                    "Sustainable livelihoods—whether a solo bench, a growing repair shop, or an IOM/agency-supported "
                    "youth/livelihood hub—depend on fair pricing, clear accountability, and repeat trust."
                ),
                "core_explanation": (
                    "PROFESSIONAL SHOP & PARTNER STANDARDS:\n"
                    "- Clear Quoting: Break down replacement part cost, labor/service fee, and turnaround estimate upfront—never surprise a client with hidden fees after finishing.\n"
                    "- Fair Warranty Policy: State warranty duration and exact terms clearly (e.g., covers defective part/workmanship on the repaired item, excluding new physical impact, liquid damage, or unauthorized tampering).\n"
                    "- Recordkeeping & Accountability: Keep clean intake/repair/QA logs so every device handed over is tested, documented, and traceable.\n\n"
                    "HANDOVER & TRUST PILLARS:\n"
                    "Pillar            | What Builds Lasting Trust\n"
                    "------------------+-------------------------------------------------------------\n"
                    "Upfront Quote     | Clear part + labor breakdown & turnaround before repair\n"
                    "Written Warranty  | Clear coverage period & exclusions (impact/liquid/tamper)\n"
                    "Final QA + Log    | Full function check + signed intake/handover record"
                ),
                "step_by_step_field_guide": (
                    "PRE-HANDOVER CHECK:\n"
                    "- Re-test power, charging, display/touch, cameras, audio/mics, Wi-Fi/SIM, and sensors after final assembly.\n\n"
                    "QUOTING & HANDOVER STEPS:\n"
                    "1. Present a clear quote (part option, labor, and estimated completion time) and get approval before ordering/fitting parts.\n"
                    "2. Complete post-repair functional testing and clean exterior surfaces/ports.\n"
                    "3. Walk the customer through the working device, explain care & warranty terms clearly, and log the completed job.\n\n"
                    "POST-HANDOVER CHECK:\n"
                    "- File the job record and note any recommended follow-up (such as battery health or protective case/glass)."
                ),
                "safety_and_traps": (
                    "- TRAP (Vague Verbal Promises): Unwritten promises lead to arguments over what was included or warranted.\n"
                    "- TRAP (Skipping Final QA After Closing): A loose cable or uncalibrated sensor caught before handover saves an angry return visit."
                ),
                "diagram_or_visual_guide": (
                    "[Clear Quote + Approval] ---> [Careful Repair + Full Post-QA]\n"
                    "                           ---> [Clear Warranty + Logged Handover]"
                ),
                "real_life_scenario": (
                    "A repeat customer brings a second phone and recommends your shop to a local NGO/livelihood "
                    "coordinator because you always give honest quotes, never overcharge, test every button and camera "
                    "before handover, and stand behind your work."
                ),
                "practice_activity": (
                    "Draft a simple 1-page repair ticket & handover summary template including intake tests, quoted "
                    "cost, post-repair QA checks, and warranty terms."
                ),
                "checkpoint_questions": (
                    "1. Why should you separate part and labor/service expectations clearly before starting a repair?\n"
                    "2. What kinds of post-repair events are typically excluded from a standard repair warranty?\n"
                    "3. How do consistent intake and QA logs support long-term business and partner credibility?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Liquid/Board Diagnostics & Shop Operations Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Smartphone Repair Specialist QR Certificate.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="A customer brings in a phone that was dropped into water 20 minutes ago. What is the safest immediate action?",
            option_a="Keep it plugged into a charger to dry it out faster",
            option_b="Ensure it is powered off and unplugged, isolate/disconnect the battery safely when opened, inspect/clean corrosion carefully, and set realistic expectations",
            option_c="Pack it tightly in uncooked rice and seal it in an airtight bag for a week",
            option_d="Apply high heat-gun air directly to the battery",
            correct_answer="B",
            explanation="Avoiding power/charging on wet electronics prevents short circuits, and proper inspection/cleaning addresses corrosion safely while setting honest expectations.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="Which practice best supports long-term customer trust and livelihood/partner credibility in a repair shop?",
            option_a="Clear upfront quotes, thorough post-repair QA testing, honest risk communication, and clear warranty terms",
            option_b="Hiding repair costs until after the phone is glued shut",
            option_c="Skipping post-repair checks to rush devices out",
            option_d="Making up vague guarantees with no written record",
            correct_answer="A",
            explanation="Transparency, thorough QA, and clear terms build lasting reputation and sustainable operations.",
        )

        # =====================================================================
        # GLOSSARY TERMS (14 TERMS ACROSS TIER 1, TIER 2 & TIER 3)
        # =====================================================================
        glossary_items = [
            ("safety", "ESD", "Electrostatic Discharge", "Sudden transfer of static electricity between surfaces at different potentials.", "Wear a grounded wrist strap on an ESD mat when handling exposed boards/flexes.", True, 1),
            ("equipment", "FPC", "Flexible Printed Circuit", "Thin flexible ribbon/connector assembly linking components to the logic board.", "Release latches gently and never pull directly on a ribbon cable.", True, 2),
            ("equipment", "LCD vs. OLED", "Liquid Crystal vs. Organic Light-Emitting Diode Display", "LCD uses a backlight layer; OLED/AMOLED pixels emit their own light.", "Guides part selection, careful prying, and pressure/heat caution.", True, 3),
            ("tools", "USB Amp Meter", "USB Voltage & Current Tester", "Measures charging voltage (V) and current draw (A) between charger and device.", "Helps spot faulty cables, dirty ports, or weak charging early.", True, 4),
            ("general", "IMEI", "International Mobile Equipment Identity", "Unique 15-digit identifier associated with a mobile device.", "Useful for device identification, records, and legitimacy checks.", True, 5),
            ("safety", "FRP / Activation Lock", "Factory Reset / Account Activation Protection", "Security lock requiring prior authorized account credentials after a reset.", "Requires legitimate owner verification and ethical handling.", True, 6),
            ("equipment", "Li-Ion Pouch Cell", "Lithium-Ion Rechargeable Battery", "High-energy battery cell sensitive to puncture, crushing, over-heat, or swelling.", "Never pry with sharp metal or apply excessive heat; keep fire-safe bin ready.", False, 7),
            ("business", "Pre-Repair Intake Check", "Baseline Functional & Cosmetic Inspection", "Testing and logging device condition and existing faults before repair begins.", "Protects technicians and customers against misunderstandings after repair.", False, 8),
            ("equipment", "Charging Sub-Board", "Lower Port & Charging Circuit Module", "Small board/flex housing the charging port, mic, or antenna contacts in many models.", "Allows clean modular replacement when a port or sub-circuit is damaged.", False, 9),
            ("business", "Firmware / Recovery Mode", "Low-Level Software Boot & Restore State", "Diagnostic or restore mode used for official OS updates or recovery.", "Requires exact model matching, steady power, and data-backup awareness.", False, 10),
            ("safety", "Corrosion / Liquid Triage", "Moisture & Oxidation Inspection/Cleaning", "Checking and cleaning conductive/corrosive residue after liquid exposure.", "Prevents shorts and sets realistic expectations on liquid-damaged devices.", False, 11),
            ("business", "Post-Repair QA", "Quality Assurance Verification Checklist", "Systematic check of power, charging, display, touch, cameras, audio, and sensors.", "Ensures every repaired phone is ready before client handover.", False, 12),
            ("business", "Itemized Quote", "Transparent Breakdown of Parts & Service", "Clear upfront pricing separating replacement parts and repair/diagnostic work.", "Prevents billing surprises and builds customer confidence.", False, 13),
            ("business", "Warranty Scope", "Defined Coverage & Exclusions After Repair", "Clear statement of what post-repair issues are covered and what is excluded.", "Protects both the customer and the repair business/partner hub.", False, 14),
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
                "including diagrams, reference tables, 14 glossary terms, and quizzes!"
            )
        )