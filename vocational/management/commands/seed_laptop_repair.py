# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_laptop_repair.py
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
        "Seeds the complete 3-tier Laptop & PC Hardware Repair course, "
        "diagrams, reference tables, glossary, and assessments."
    )

    def handle(self, *args, **options):
        cat_name = "Laptop & PC Hardware Repair"
        cat_slug = "laptop-pc-hardware-repair"
        cat_desc = (
            "Practical laptop and desktop diagnostics, safe battery/power isolation, RAM, "
            "SSD/HDD, display, hinge, and cooling servicing, OS/UEFI recovery, power-rail "
            "troubleshooting, and honest client repair operations."
        )

        category = TradeCategory.objects.filter(slug=cat_slug).first()
        if category:
            category.slug = cat_slug
            category.name = cat_name
            category.description = cat_desc
            if hasattr(category, "name_en"):
                category.name_en = cat_name
            if hasattr(category, "description_en"):
                category.description_en = cat_desc
            category.save()
        else:
            create_kwargs = {
                "slug": cat_slug,
                "name": cat_name,
                "description": cat_desc,
            }
            if hasattr(TradeCategory, "name_en"):
                create_kwargs["name_en"] = cat_name
            if hasattr(TradeCategory, "description_en"):
                create_kwargs["description_en"] = cat_desc
            category = TradeCategory.objects.create(**create_kwargs)

        # =====================================================================
        # TIER 1 (FREE): FOUNDATION, BENCH SAFETY & INTAKE DIAGNOSTICS
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-pc-repair-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Laptop & PC Repair — Tier 1: Bench Safety, Intake Triage & Core Terminology",
                "description": (
                    "FREE TIER: Build safe hardware habits with AC/battery isolation, ESD protection, "
                    "essential technician tools, structured intake & POST checks, data-backup care, "
                    "and core laptop/PC terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Laptop & PC Bench Readiness Record",
                "required_tools": (
                    "ESD-Safe Mat & Wrist Strap, Precision & Torx/Phillips Driver Set, "
                    "Plastic Spudgers & Pry Picks, Digital Multimeter, Flashlight/Magnifier, "
                    "Intake & Data-Risk Checklist"
                ),
                "safety_guidelines": (
                    "1. Unplug the AC adapter/power cord and disconnect or isolate the internal/external battery before opening or probing.\n"
                    "2. Ground yourself with an ESD strap on an ESD mat before touching RAM, SSDs, or motherboards.\n"
                    "3. Log existing physical damage, missing keys/screws, and customer data risks before starting work."
                ),
                "field_tips_summary": (
                    "Never open a live or plugged-in laptop, always check external power/adapter/peripherals "
                    "and log pre-existing faults at intake, and back up or warn clients before any OS/drive change."
                ),
                "course_glossary_overview": (
                    "Covers POST, BIOS/UEFI, RAM (DDR), NVMe/SATA SSD, DC Jack/PD, thermal paste, "
                    "and ESD so technicians communicate clearly and diagnose accurately."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Bench Safety, Intake Checks & Core PC Terminology",
                "tier": "tier_1",
                "summary": "Safe power/ESD habits, intake & boot triage, data protection, and starter terms.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: Bench Safety, Power Isolation, Intake Checks & Data Protection",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Isolate AC power and battery circuits safely before opening laptops or desktops.\n"
                    "- Run a structured intake check covering power/charging, display, keyboard/trackpad, ports, audio, and storage/boot behavior.\n"
                    "- Protect customer data and document pre-existing damage before beginning repairs."
                ),
                "why_it_matters": (
                    "Opening a laptop with residual battery/AC power can short a board or damage a display flex, "
                    "while skipping intake checks invites blame for cracked hinges, dead ports, or pre-existing "
                    "data/boot issues."
                ),
                "core_explanation": (
                    "LAPTOP & PC INTAKE & SAFETY MATRIX:\n"
                    "- Power Isolation: Unplug charger/power cable, remove removable batteries, and disconnect internal battery connectors as soon as the bottom case is off.\n"
                    "- ESD & Workspace Care: Work on a grounded ESD mat with a wrist strap, keep drinks/liquids away from the bench, and organize screws by length and location.\n"
                    "- Baseline Intake Check: Inspect chassis hinges, corners, ports, and screen for cracks/dents/liquid signs; test power-on, display image/backlight, keyboard/touchpad, USB/charging ports, Wi-Fi/audio, and boot status.\n"
                    "- Data & Liability Care: Remind clients to back up important files before OS/drive/repair work and log existing faults on the intake form.\n\n"
                    "INTAKE TRIAGE CHECKLIST:\n"
                    "Check Area    | Key Inspection Points Before Opening\n"
                    "--------------+-------------------------------------------------------------\n"
                    "Chassis/Hinge | Hinge stiffness/cracks, corner dents, swell, missing screws\n"
                    "Power & Boot  | Adapter/port state, POST/BIOS screen, OS boot & battery health\n"
                    "I/O & Data    | Display/touch, keyboard/trackpad, USB/audio/Wi-Fi + backup notice"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Clear the bench, put on your ESD wrist strap on a grounded mat, and keep a screw map/tray ready.\n\n"
                    "INTAKE & SAFETY STEPS:\n"
                    "1. Inspect the laptop or PC case for hinge stress, cracks, swollen batteries, loose/missing screws, or liquid stains and record them.\n"
                    "2. Check power/charging behavior, screen display, keyboard/trackpad, ports, fan/heat behavior, and boot/login response.\n"
                    "3. Advise the client on data backup and record any pre-existing faults before opening.\n"
                    "4. Unplug external power, remove bottom cover screws in order, and disconnect the battery lead before touching internal parts.\n\n"
                    "POST-INTAKE CHECK:\n"
                    "- Confirm power is isolated and your intake notes match the actual condition of the machine."
                ),
                "safety_and_traps": (
                    "- TRAP (Working With Battery Still Connected): Leaving the battery plugged in while unplugging LCD, keyboard, or Wi-Fi cables can cause shorts or backlight/board damage.\n"
                    "- TRAP (Ignoring Cracked Hinge Mounts): Opening a laptop lid with a seized hinge or cracked brass insert can rip the display bezel or palmrest apart.\n"
                    "- TRAP (Assuming Data Is Safe During Repair): Drops, drive faults, or OS recovery can affect data—always set expectations clearly."
                ),
                "diagram_or_visual_guide": (
                    "[Machine Arrives] ---> [Log Hinges/Case/Faults + Data Notice]\n"
                    "                 ---> [Unplug AC + ESD Mat/Strap + Open Safely]\n"
                    "                 ---> [Disconnect Battery Before Internal Work]"
                ),
                "real_life_scenario": (
                    "A client brings in a laptop with a dim/flickering screen. At intake, you notice a loose hinge "
                    "on the right side and a USB port that feels wobbly, and you note both on the intake sheet. "
                    "After servicing the display/cable, the client sees the hinge still needs attention—your intake "
                    "record shows you spotted it from the start and gives a clear basis for a follow-up quote."
                ),
                "practice_activity": (
                    "Perform a 15-minute intake inspection on a laptop or desktop: check case/hinges/ports, test "
                    "power/display/input/boot behavior, and write an intake summary with pre-existing issues and data advice."
                ),
                "checkpoint_questions": (
                    "1. Why should you disconnect the internal battery after opening a laptop case and before unplugging cables?\n"
                    "2. Why is logging existing hinge cracks or port wear at intake so important?\n"
                    "3. What should you tell a client about data before starting hardware or OS troubleshooting?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Core Laptop & PC Hardware, BIOS/UEFI & Storage Terminology",
                "estimated_minutes": 40,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Explain essential PC/laptop terms including POST, BIOS/UEFI, RAM, SSD (NVMe/SATA), "
                    "DC jack/USB-C PD, and thermal paste.\n"
                    "- Match symptoms and parts accurately when diagnosing or quoting repairs."
                ),
                "why_it_matters": (
                    "Ordering DDR4 instead of DDR5, NVMe instead of SATA (or vice versa), or the wrong charger "
                    "voltage/wattage wastes money and delays repairs. Knowing core terms makes troubleshooting "
                    "faster and clearer."
                ),
                "core_explanation": (
                    "CORE LAPTOP & PC TERMINOLOGY:\n"
                    "- POST (Power-On Self-Test): Built-in hardware check run when powered on before loading the operating system.\n"
                    "- BIOS / UEFI: Low-level firmware stored on the board that initializes hardware, sets boot order, and manages security/power options.\n"
                    "- RAM (Random Access Memory): Fast temporary working memory; capacity and speed strongly affect multitasking.\n"
                    "- SSD (NVMe vs. SATA) / HDD: Solid-state drives have no moving platters and are much faster/more shock-resistant than mechanical HDDs; verify interface/form factor before buying.\n"
                    "- DC Jack / USB-C PD: Power input port or USB-C Power Delivery charging standard—match voltage, wattage, and connector/protocol.\n"
                    "- Thermal Paste / Thermal Pads: Heat-transfer compound/pads bridging CPU/GPU/VRMs to the heatsink.\n\n"
                    "SUBSYSTEM & SPEC REFERENCE:\n"
                    "Term / Component | Role in System / Repair\n"
                    "-----------------+-------------------------------------------------------------\n"
                    "POST & BIOS/UEFI | Pre-OS hardware check & firmware configuration/boot control\n"
                    "RAM & SSD/HDD    | Active working memory & persistent storage (NVMe/SATA)\n"
                    "DC Jack / PD / TP| Power entry/negotiation & CPU-to-heatsink thermal transfer"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Check the exact model number, charger rating (V / W), and current RAM/storage specs before buying upgrades or parts.\n\n"
                    "SPEC & TERMINOLOGY CHECK STEPS:\n"
                    "1. Check whether the machine passes POST / enters BIOS/UEFI or stops with no display/beep/LED codes.\n"
                    "2. Identify exact RAM type/slots and storage type (M.2 NVMe, M.2 SATA, 2.5-inch SATA) before recommending upgrades.\n"
                    "3. Check power adapter voltage/wattage and charging port condition when diagnosing power/charging faults.\n"
                    "4. Note fan noise, dust buildup, or high temperatures that point toward thermal/cooling service.\n\n"
                    "POST-CHECK:\n"
                    "- Record exact specs and findings clearly so quotes and replacements match the machine."
                ),
                "safety_and_traps": (
                    "- TRAP (Buying the Wrong Charger or RAM/SSD Type): Mismatched RAM generation, wrong SSD interface, or an underpowered charger causes boot failure, throttling, or charging issues.\n"
                    "- TRAP (Confusing 'No Windows Boot' With 'Dead Hardware'): A laptop that enters BIOS/UEFI but fails to load Windows may have a boot-order, OS, or drive issue rather than a dead motherboard.\n"
                    "- TRAP (Reusing Dried-Out Thermal Paste): Leaving old, chalky paste or torn thermal pads after removing a heatsink leads to overheating."
                ),
                "diagram_or_visual_guide": (
                    "[Power On] ---> [POST / BIOS-UEFI Check] ---> [Storage / OS Boot]\n"
                    "                |\n"
                    "                +---> Checks RAM, Power/Charging & Thermal/Cooling Health"
                ),
                "real_life_scenario": (
                    "A client says their laptop 'won't turn on at all.' When you press power, the keyboard backlight "
                    "or indicator lights come on and you can access BIOS/UEFI, but Windows shows an error. Knowing the "
                    "difference between a dead power rail and a boot/OS/drive issue saves time and gives an accurate diagnosis."
                ),
                "practice_activity": (
                    "Write clear definitions and one field use for: POST, BIOS/UEFI, RAM, NVMe vs. SATA SSD, "
                    "and thermal paste."
                ),
                "checkpoint_questions": (
                    "1. What is POST, and why is checking whether a laptop reaches BIOS/UEFI helpful during diagnosis?\n"
                    "2. Why must you check both form factor and interface (such as NVMe vs. SATA) before buying an SSD?\n"
                    "3. What is the job of thermal paste between a processor and heatsink?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Laptop & PC Bench Safety & Intake Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify your grasp of bench safety, intake checks, and core laptop/PC terms.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="Before opening a laptop case and disconnecting internal cables, what is the safest bench practice?",
            option_a="Unplug AC power, work with ESD protection, log existing conditions/data risks, and disconnect the battery once inside",
            option_b="Leave the charger plugged in so you can see lights while prying internal cables",
            option_c="Skip recording pre-existing hinge cracks or port damage until after the job",
            option_d="Use a wet cloth to wipe inside the open motherboard area",
            correct_answer="A",
            explanation="Isolating power, protecting against ESD, and logging intake/data risks prevent damage and disputes.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="Which built-in hardware check runs when a computer powers on before loading the operating system?",
            option_a="POST (Power-On Self-Test)",
            option_b="Thermal paste",
            option_c="Defragmentation",
            option_d="Screen calibration",
            correct_answer="A",
            explanation="POST (Power-On Self-Test) checks core hardware readiness during startup before OS boot.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): HARDWARE UPGRADES, DISPLAY/HINGE, COOLING & OS/UEFI
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-pc-repair-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Laptop & PC Repair — Tier 2: Upgrades, Displays, Hinges, Cooling & OS/UEFI",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Upgrade RAM and SSDs, replace laptop screens and repair "
                    "hinges/cables, clean fans and renew thermal paste, perform OS/driver/BIOS/UEFI recovery, "
                    "and verify full system stability."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 12,
                "credential_awarded": "Tier 2 Practical Laptop & PC Technician Certificate & Interim Transcript",
                "required_tools": (
                    "All Tier 1 tools plus Isopropyl Alcohol (IPA) & Lint-Free Wipes, Quality Thermal Paste "
                    "& Pads, Compressed Air / Soft Brush (used carefully with fan held), Bootable OS/Diagnostic "
                    "USB Media, Precision Pry Tools"
                ),
                "safety_guidelines": (
                    "1. Always isolate AC power and disconnect the battery before seating/removing RAM, SSDs, display cables, or heatsinks.\n"
                    "2. Hold cooling fan blades gently when cleaning with air so overspinning does not damage fan bearings or generate back-voltage.\n"
                    "3. Back up client data and verify exact model/firmware/driver compatibility before OS reinstalls or BIOS/UEFI updates."
                ),
                "field_tips_summary": (
                    "Reseat memory/storage cleanly, never force hinges or display bezels, clean old thermal "
                    "paste evenly before applying a thin fresh layer, and run stress/function checks before handover."
                ),
                "course_glossary_overview": (
                    "Covers SO-DIMM/RAM seating, NVMe/SATA migration, eDP/LVDS display panels & hinges, "
                    "thermal throttling/paste application, and clean OS/driver/UEFI setup."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: RAM, Storage, Display/Hinge & Thermal Cooling Service",
                "tier": "tier_2",
                "summary": "Perform clean memory/storage upgrades, screen/hinge repairs, and thermal servicing.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: RAM & SSD Upgrades, Data Migration & Boot Verification",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Install or reseat RAM modules and NVMe/SATA SSDs cleanly without damaging slots or retention clips.\n"
                    "- Plan safe data transfer/migration and verify full capacity and boot stability.\n"
                    "- Troubleshoot basic 'no boot after upgrade' symptoms like unseated RAM or loose drives."
                ),
                "why_it_matters": (
                    "Upgrading slow mechanical drives to SSDs and adding appropriate RAM is one of the highest-value, "
                    "most common repairs—delivering noticeable speed gains when done cleanly and safely."
                ),
                "core_explanation": (
                    "MEMORY & STORAGE UPGRADE STANDARDS:\n"
                    "- RAM Seating: Align the key notch on the module with the slot key, insert at the required angle, press firmly until side clips lock, and lay flat (on angled SO-DIMM slots).\n"
                    "- SSD Installation: Align M.2 connector notch, seat gently without forcing, secure with the retention screw, or mount 2.5-inch drives cleanly.\n"
                    "- Data & OS Check: Confirm whether the client needs a fresh OS install or data/system transfer, and verify total RAM and drive recognition in BIOS/UEFI and the OS."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Unplug charger, open case, disconnect battery, and ground with ESD strap.\n\n"
                    "UPGRADE & VERIFICATION STEPS:\n"
                    "1. Remove or install RAM module(s) by aligning the key notch and locking clips evenly.\n"
                    "2. Install or replace the SSD/storage drive and secure its mounting screw/bracket cleanly.\n"
                    "3. Reconnect the battery and test power-on—confirm the new RAM and drive appear in BIOS/UEFI.\n"
                    "4. Complete OS installation or data transfer, install key drivers, and verify normal boot and file access.\n\n"
                    "POST-UPGRADE CHECK:\n"
                    "- Close the chassis, torque screws properly, and confirm smooth startup without errors."
                ),
                "safety_and_traps": (
                    "- TRAP (Forcing RAM Backward): The notch prevents backward insertion—forcing it can crack the slot or module.\n"
                    "- TRAP (Stripping Tiny M.2 Screws): Using an ill-fitting screwdriver can strip soft M.2 screw heads.\n"
                    "- TRAP (Forgetting to Reconnect Battery Before Testing): Always reconnect the battery and verify assembly before closing up."
                ),
                "diagram_or_visual_guide": (
                    "[Isolate Power & ESD] ---> [Align Notch & Seat RAM / SSD] ---> [Verify in BIOS/UEFI]\n"
                    "                     ---> [OS / Data Setup & Boot Test]"
                ),
                "real_life_scenario": (
                    "A client complains that a 4GB RAM / mechanical-HDD laptop takes several minutes to boot and freezes "
                    "when opening a browser and spreadsheets. Upgrading to an SSD and matching RAM capacity (where "
                    "supported) transforms responsiveness—provided you verify compatibility and back up data first."
                ),
                "practice_activity": (
                    "List the steps to safely upgrade RAM and an M.2 SSD on a laptop, including two checks you run "
                    "before handing the laptop back."
                ),
                "checkpoint_questions": (
                    "1. How does the notch on a RAM stick or M.2 SSD help prevent wrong insertion?\n"
                    "2. Why is checking BIOS/UEFI a helpful step right after installing new RAM or an SSD?\n"
                    "3. What should you do before wiping or replacing a client's primary storage drive?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=2,
            defaults={
                "title": "Step 4: Laptop Display Panels, Video Cables & Hinge/Bezel Repair",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Diagnose cracked/lined screens, loose/damaged display cables, and stiff or broken hinges.\n"
                    "- Remove bezels and display panels carefully without cracking glass or tearing display/webcam cables.\n"
                    "- Test display clarity, brightness, and hinge movement smoothly before final assembly."
                ),
                "why_it_matters": (
                    "Laptop screens and hinges are delicate and expensive. Yanking a display cable with power on "
                    "or forcing a stiff hinge can ruin a new panel or crack the palmrest."
                ),
                "core_explanation": (
                    "DISPLAY & HINGE SERVICE RULES:\n"
                    "- Power Off First: Always disconnect AC and battery before unplugging or seating display cables.\n"
                    "- Hinge Tension & Anchors: Stiff or seized hinges put heavy leverage on small brass screw inserts in the lid or palmrest—inspect mounts and ease hinge stiffness where needed.\n"
                    "- Panel & Cable Care: Unclip bezels gently, release adhesive/screws carefully, remove connector tape/latches without pulling wires, and test image/brightness before snapping trim shut."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Disconnect charger and battery; confirm replacement panel connector pinout, size, resolution, and mount type match.\n\n"
                    "DISPLAY & HINGE STEPS:\n"
                    "1. Carefully release front bezel clips/adhesive without prying sharply into the LCD panel.\n"
                    "2. Unscrew/release panel mounts and hinge screws; support the lid so it doesn't snap backward.\n"
                    "3. Disconnect the display cable carefully, install the replacement panel/hinge hardware, and reconnect the cable securely.\n"
                    "4. Reconnect battery temporarily, power on to test display image, brightness, and camera/hinge motion, then finish bezel/screw assembly.\n\n"
                    "POST-REPAIR CHECK:\n"
                    "- Open and close the lid smoothly while checking for uniform screen image and no bezel gaps."
                ),
                "safety_and_traps": (
                    "- TRAP (Unplugging Display Cable With Battery Connected): Can cause shorts or blow display/backlight circuits.\n"
                    "- TRAP (Forcing a Seized Hinge): Opening a jammed hinge without freeing/repairing mounts can rip brass inserts straight out of plastic.\n"
                    "- TRAP (Flexing the Panel Hard While Removing Tape): Bending a thin LCD/LED panel can cause pressure lines or cracks."
                ),
                "diagram_or_visual_guide": (
                    "[Isolate AC & Battery] ---> [Gentle Bezel & Hinge Access] ---> [Clean Cable Swap]\n"
                    "                      ---> [Test Display & Hinge Motion] ---> [Final Trim & Screw Check]"
                ),
                "real_life_scenario": (
                    "A laptop lid pops open with a cracking sound and the lower corner of the screen frame separates. "
                    "Inspection shows a seized/broken hinge mount stressing the housing. Repairing/securing the hinge "
                    "and replacing the damaged panel/trim restores smooth lid operation without repeating the break."
                ),
                "practice_activity": (
                    "Write out the key precautions when replacing a laptop screen and inspecting hinges, including "
                    "how you test before sealing the bezel."
                ),
                "checkpoint_questions": (
                    "1. Why must AC power and the battery be disconnected before handling display cables?\n"
                    "2. What happens if a stiff or broken laptop hinge is ignored during a screen repair?\n"
                    "3. Why should you test the screen and lid movement before snapping the bezel completely shut?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=3,
            defaults={
                "title": "Step 5: Thermal Cleaning, Heatsink Service & Repasting",
                "estimated_minutes": 50,
                "learning_objectives": (
                    "- Spot signs of thermal throttling, loud fan noise, dust blockage, and dried thermal paste.\n"
                    "- Clean heatsinks and fans safely and apply fresh thermal paste evenly.\n"
                    "- Verify cooler temperatures and quieter, steadier performance under load."
                ),
                "why_it_matters": (
                    "Dust-clogged heatsinks and dried-out paste trap heat inside laptops and PCs—causing loud fans, "
                    "sudden thermal shutdowns, sluggish performance, and premature component wear."
                ),
                "core_explanation": (
                    "THERMAL & COOLING SERVICE STANDARDS:\n"
                    "- Symptoms: Fan spinning loudly at idle/light tasks, hot palmrest/exhaust, sudden shutoffs under workload, or CPU/GPU slowing down (thermal throttling).\n"
                    "- Clean & Repaste: Remove dust lint from heatsink fins and fan blades, clean old thermal paste thoroughly from CPU/GPU dies and heatsink bases with lint-free wipes/IPA, and apply a controlled, thin, even layer of fresh thermal paste.\n"
                    "- Even Mounting Pressure: Tighten heatsink screws gradually in sequence/cross-pattern per design so contact pressure is even.\n\n"
                    "THERMAL SERVICE REFERENCE:\n"
                    "Symptom / Step    | Key Action / Standard\n"
                    "------------------+-------------------------------------------------------------\n"
                    "Overheat / Thrott | Check fan airflow, fin dust blockage & dried paste/pads\n"
                    "Fan & Fin Clean   | Hold fan blades gently; clear lint from fins & vents\n"
                    "Paste & Mounting  | Clean old paste with IPA; thin even coat + even screw torque"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Power off, unplug AC, and disconnect the battery.\n\n"
                    "COOLING SERVICE STEPS:\n"
                    "1. Remove fan/heatsink assembly carefully (holding fan blades so they do not spin rapidly) and clear dust/lint from fin vents.\n"
                    "2. Wipe away old dried thermal paste from processor and heatsink surfaces cleanly; check thermal pads.\n"
                    "3. Apply a proper, controlled amount of fresh thermal paste to the processor die(s).\n"
                    "4. Re-seat the heatsink evenly, tighten screws gradually without over-torquing, reconnect fan and battery, and test temperatures/fan behavior.\n\n"
                    "POST-SERVICE CHECK:\n"
                    "- Confirm the fan spins smoothly and airflow exits the vent cleanly."
                ),
                "safety_and_traps": (
                    "- TRAP (Too Much or Too Little Thermal Paste): Too little leaves dry spots; excess can squeeze out onto nearby components or insulate poorly.\n"
                    "- TRAP (Spinning Fans Fast With Air Blasts): Overspinning a DC fan can wear bearings or induce voltage back into the board.\n"
                    "- TRAP (Uneven Heatsink Tightening): Tightening one screw all the way down first can tilt the cooler and leave poor contact."
                ),
                "diagram_or_visual_guide": (
                    "[Dust & Old Paste] ---> [Clean Fins/Fan + Wipe Old Paste]\n"
                    "                   ---> [Apply Thin Fresh Paste + Even Screw Tension]\n"
                    "                   ---> [Verify Cooler, Quieter Operation]"
                ),
                "real_life_scenario": (
                    "A client's laptop shuts down abruptly during video calls or spreadsheet work and blows hot air "
                    "from the side vent. Inside, a thick mat of dust blocks the heatsink fins and the old paste is "
                    "dry and cracked. Cleaning the fins/fan and repasting restores normal cooling and stops the shutdowns."
                ),
                "practice_activity": (
                    "Write out the steps for cleaning a laptop heatsink/fan and applying fresh thermal paste, "
                    "including why you hold the fan blade during cleaning."
                ),
                "checkpoint_questions": (
                    "1. What happens when a heatsink's cooling fins become blocked with dust?\n"
                    "2. Why should you hold cooling fan blades steady when blowing out dust?\n"
                    "3. Why apply a thin, even layer of thermal paste rather than a huge blob?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: OS Recovery, Drivers & Firmware Setup",
                "tier": "tier_2",
                "summary": "Perform clean OS installs, driver updates, and safe BIOS/UEFI checks with data care.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 6: OS Installation, Drivers, BIOS/UEFI Diagnostics & Safe Data Handling",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Diagnose OS corruption, startup errors, and missing/faulty drivers.\n"
                    "- Perform clean OS setup, driver installation, and basic BIOS/UEFI boot/security checks.\n"
                    "- Protect client files and privacy before and after software changes."
                ),
                "why_it_matters": (
                    "A fresh OS or wrong driver can leave Wi-Fi, audio, trackpad, or graphics dead—or wipe "
                    "important client data if rushed without a backup check."
                ),
                "core_explanation": (
                    "OS, DRIVER & BIOS/UEFI DISCIPLINE:\n"
                    "- Backup First: Confirm client data backup before formatting/reinstalling an OS.\n"
                    "- Clean Boot & Drivers: Check boot order/UEFI mode (e.g., UEFI vs. legacy where applicable), install the OS cleanly, and install chipset, display, Wi-Fi/LAN, and audio drivers from trusted sources.\n"
                    "- BIOS/UEFI Caution: Only update BIOS/UEFI when needed for a documented fix/compatibility, with steady power and exact model match—never interrupt a firmware flash."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Confirm customer data backup status and connect reliable AC power.\n\n"
                    "OS & DRIVER STEPS:\n"
                    "1. Verify BIOS/UEFI drive detection, boot settings, and system time/date.\n"
                    "2. Back up/transfer user files as agreed before any drive format or OS installation.\n"
                    "3. Complete OS installation and install required drivers (Wi-Fi, chipset, display, audio, trackpad).\n"
                    "4. Test internet/Wi-Fi, sound, display scaling/brightness, USB ports, and sleep/wake/restart behavior.\n\n"
                    "POST-SETUP CHECK:\n"
                    "- Confirm no critical hardware devices show driver errors and client data/accounts are handled cleanly."
                ),
                "safety_and_traps": (
                    "- TRAP (Formatting Without Checking Backups): Wiping a drive without confirming backups can cause permanent loss of client work or photos.\n"
                    "- TRAP (Unnecessary Risky BIOS/UEFI Flashes): Updating firmware with unstable power or wrong model files can brick the board.\n"
                    "- TRAP (Leaving Missing Wi-Fi/Audio Drivers): Handing back a laptop without Wi-Fi or sound drivers creates immediate frustration."
                ),
                "diagram_or_visual_guide": (
                    "[Backup Check + AC Power] ---> [BIOS/UEFI & Clean OS Install]\n"
                    "                          ---> [Drivers + I/O / Sleep / Restart QA]"
                ),
                "real_life_scenario": (
                    "A laptop loops on a startup repair screen after a failed system update. You explain data-backup "
                    "options to the client, perform a clean OS recovery on steady power, install the missing Wi-Fi and "
                    "audio drivers, and verify normal boot before handover."
                ),
                "practice_activity": (
                    "List 5 post-install checks you run after reinstalling an OS and drivers on a laptop."
                ),
                "checkpoint_questions": (
                    "1. Why verify data backup before formatting or reinstalling an operating system?\n"
                    "2. Which drivers should you verify right after an OS setup so the laptop is usable day-to-day?\n"
                    "3. Why is steady power essential during firmware/BIOS/UEFI operations?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Practical Upgrades, Display/Hinge, Cooling & OS Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test your practical laptop/PC upgrade, display/hinge, thermal, and OS setup judgment.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="A laptop shuts down under load and runs hot. Inside, the heatsink fins are packed with dust and the thermal paste is dried out. What should you do?",
            option_a="Isolate power/battery, clean dust from fins/fan (holding fan blades steady), remove old paste, apply a thin even layer of fresh paste, and test cooling",
            option_b="Pour water into the exhaust vent to cool it down",
            option_c="Apply a thick layer of grease or cooking oil to the CPU",
            option_d="Disable the cooling fan permanently in BIOS",
            correct_answer="A",
            explanation="Clearing dust blockages, renewing thermal paste evenly, and checking fan operation restores safe heat dissipation.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="Why must AC power and the battery be isolated before unplugging or seating a laptop display cable?",
            option_a="To prevent short circuits or backlight/display board damage while working near live power rails",
            option_b="Because display cables cannot be disconnected when the battery is removed",
            option_c="To erase the SSD automatically",
            option_d="Isolation is only needed on desktop towers",
            correct_answer="A",
            explanation="Isolating AC and battery power before handling display connectors prevents shorts and circuit damage.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): POWER/BOARD DIAGNOSTICS & SHOP / IOM READINESS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-pc-repair-tier-3-professional",
            defaults={
                "category": category,
                "title": "Laptop & PC Repair — Tier 3: Power/Board Diagnostics & Shop / Partner Mastery",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Troubleshoot no-power/charging & peripheral faults methodically; "
                    "quote repairs honestly; manage part/warranty boundaries; and build a reliable repair "
                    "livelihood or partner-ready service operation for QR certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 10,
                "credential_awarded": "Tier 3 Master Laptop & PC Technician QR Certificate & Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus Digital Multimeter, Known-Good Test Charger/RAM/SSD, "
                    "Magnifier/Inspection Lamp, Itemized Quote Sheet, Job Log & Warranty Slip"
                ),
                "safety_guidelines": (
                    "1. Unplug power immediately if you smell burning, see scorch/liquid marks, or feel abnormal heat on a DC jack/board.\n"
                    "2. Isolate faults step by step (adapter/DC jack -> battery/RAM/storage -> peripherals/board) rather than guessing or throwing parts.\n"
                    "3. Be transparent about repair feasibility, cost, and warranty boundaries before and after work."
                ),
                "field_tips_summary": (
                    "Clear diagnosis + honest pricing + clean handover testing turns first-time walk-ins into "
                    "repeat clients and credible partners for livelihood and training programs."
                ),
                "course_glossary_overview": (
                    "Covers DC Jack / Charging Path, POST / No-Boot Isolation, Keyboard/Trackpad Flex, "
                    "Itemized Quote, Warranty Scope, and Handover QA."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Power/Peripheral Diagnostics & Professional Shop Operations",
                "tier": "tier_3",
                "summary": "Diagnose power and peripheral faults cleanly and run transparent quotes, warranties, and QA.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 7: Power/Charging Faults, Keyboard/Port Servicing & Systematic Fault Isolation",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Diagnose 'no power / won't charge' and dead keyboard/trackpad/port symptoms systematically.\n"
                    "- Isolate external charger/DC-in issues from internal battery, memory, storage, or motherboard faults.\n"
                    "- Know when to escalate or explain board-level limits honestly."
                ),
                "why_it_matters": (
                    "'Laptop won't turn on or charge' is one of the highest-stakes customer complaints. Methodical "
                    "isolation saves money on unnecessary parts and prevents risky guesswork."
                ),
                "core_explanation": (
                    "SYSTEMATIC POWER & PERIPHERAL DIAGNOSTICS:\n"
                    "- Power & Charging Path: Verify AC adapter output/condition, inspect DC barrel jack or USB-C port/cable for looseness or damage, and check whether the laptop runs/charges with battery connected or isolated.\n"
                    "- No-Boot / POST Triage: Check power LEDs, fan spin, external display output, and single-stick/known-good RAM/storage before assuming a dead motherboard.\n"
                    "- Keyboards, Trackpads & Ports: Check ribbon cable seating/latches and liquid/corrosion signs; note that many modern slim laptops rivet keyboards into the top case, affecting replacement cost and labor.\n\n"
                    "FAULT ISOLATION QUICK GUIDE:\n"
                    "Symptom                 | First Places to Inspect\n"
                    "------------------------+-------------------------------------------------------------\n"
                    "No Power / No Charge    | Adapter V/W, DC/USB-C port & cable, battery/power rail\n"
                    "Lights On, No Display   | External monitor output, RAM seating, POST/display cable\n"
                    "Dead Keys / Trackpad    | Ribbon cable & latch seating, liquid/corrosion marks"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Unplug power and wear ESD protection before opening or reseating internal connectors.\n\n"
                    "DIAGNOSTIC STEPS:\n"
                    "1. Test with a verified compatible adapter and inspect the charging port/DC jack for wobble, looseness, or damage.\n"
                    "2. Check power/charging LEDs, fan reaction, and external monitor output to separate display issues from no-POST issues.\n"
                    "3. Reseat RAM and inspect keyboard/trackpad/port flex cables and latches cleanly.\n"
                    "4. Summarize root cause, repair options, and any board-level risk clearly before proceeding.\n\n"
                    "POST-DIAGNOSTIC CHECK:\n"
                    "- Log exact test observations so the quote matches the actual fault."
                ),
                "safety_and_traps": (
                    "- TRAP (Replacing a Motherboard Before Checking Charger/RAM/Display): Always verify power adapter, RAM seating, and external display output first.\n"
                    "- TRAP (Underestimating Riveted Keyboard Labor): Riveted palmrest keyboards take significantly more time/care than screw-in keyboards—quote accurately.\n"
                    "- TRAP (Ignoring Burnt Smells or Scorched Ports): Stop immediately and inspect safely if there is heat/char damage."
                ),
                "diagram_or_visual_guide": (
                    "[No Power / Boot Fault] ---> [Adapter & Port/DC Check] ---> [LED / Fan / External Display]\n"
                    "                        ---> [RAM / Flex Seating] ---> [Clear Root-Cause Quote]"
                ),
                "real_life_scenario": (
                    "A client brings a laptop with 'no screen' and a few dead keys. Testing on an external monitor "
                    "shows the computer boots cleanly to Windows, while inspecting the top case reveals a loose "
                    "keyboard ribbon and liquid residue on the old palmrest—giving a clear, targeted repair plan."
                ),
                "practice_activity": (
                    "Write a step-by-step diagnostic checklist for a laptop that shows charging lights but gives no display."
                ),
                "checkpoint_questions": (
                    "1. Why test external display output when a laptop's built-in screen stays blank?\n"
                    "2. What should you check before suspecting a major motherboard failure on a 'won't power on' laptop?\n"
                    "3. Why does keyboard mounting style (screw-in vs. riveted palmrest) matter when quoting a repair?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 8: Honest Quoting, Warranty Boundaries & Sustainable Workshop / Partner Operations",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Prepare clear, fair repair quotes separating parts, labor/diagnostic time, and turnaround.\n"
                    "- Set clear warranty terms and explain exclusions (physical drops, liquid spills, misuse, wear) plainly.\n"
                    "- Maintain clean records that build repeat customers and livelihood/partner trust."
                ),
                "why_it_matters": (
                    "Technical skill alone doesn't sustain a business or livelihood hub—fair pricing, clear "
                    "boundaries, and reliable handover checks are what keep clients and partners coming back."
                ),
                "core_explanation": (
                    "SUSTAINABLE REPAIR SHOP & PARTNER HABITS:\n"
                    "- Transparent Quoting: State part cost, service/labor fee, and expected turnaround upfront; get client approval before ordering parts or doing paid work.\n"
                    "- Clear Warranty Boundaries: Define what is covered (e.g., workmanship or defective replacement part on the serviced item during the stated period) and what is excluded (new impact/drops, liquid spills, power surges, normal battery wear, or tampering).\n"
                    "- Handover QA & Records: Test power, charging, display, keyboard/touchpad, ports, Wi-Fi/audio, and boot before handing over, and keep clear job records for accountability and partner/livelihood reporting.\n\n"
                    "OPERATIONS & TRUST MATRIX:\n"
                    "Practice          | Why It Matters for Growth & Partners\n"
                    "------------------+-------------------------------------------------------------\n"
                    "Itemized Quote    | Prevents disputes & builds price fairness credibility\n"
                    "Clear Warranty    | Sets realistic expectations & protects against misuse claims\n"
                    "Handover QA & Log | Cuts comebacks & supports business/program records"
                ),
                "step_by_step_field_guide": (
                    "PRE-HANDOVER CHECK:\n"
                    "- Run a final check of charging, boot, display, keyboard/trackpad, USB/audio/Wi-Fi, and case screws.\n\n"
                    "QUOTING & HANDOVER STEPS:\n"
                    "1. Share a clear quote (parts, service/labor, and timeline) and confirm approval before starting.\n"
                    "2. Complete the repair and perform a full post-repair functional test.\n"
                    "3. Walk the client through the working machine, explain care & warranty terms clearly, and log the completed job.\n\n"
                    "POST-HANDOVER CHECK:\n"
                    "- Store intake, quote, and completion notes neatly for follow-up support and business tracking."
                ),
                "safety_and_traps": (
                    "- TRAP (Hidden Extra Charges at Pickup): Adding surprise fees after repair damages trust fast.\n"
                    "- TRAP (Unclear Warranty Terms): Vague 'lifetime' or undefined guarantees create costly arguments later.\n"
                    "- TRAP (Rushing Handover Without Testing Ports & Keys): Always check every key, port, and charger connection before closing the ticket."
                ),
                "diagram_or_visual_guide": (
                    "[Clear Quote + Approval] ---> [Careful Repair + Full Post-QA]\n"
                    "                           ---> [Clear Warranty + Logged Handover]"
                ),
                "real_life_scenario": (
                    "A small business or livelihood program needs 8 laptops serviced and upgraded before a training "
                    "cohort starts. Because you provide clear itemized quotes, realistic timelines, tested machines, "
                    "and clean handover records, you win ongoing work and strong referrals."
                ),
                "practice_activity": (
                    "Draft a simple 1-page laptop repair & handover sheet covering intake notes, quoted parts/labor, "
                    "final QA checks, and warranty terms."
                ),
                "checkpoint_questions": (
                    "1. Why should a client approve a clear quote before you fit replacement parts or complete paid work?\n"
                    "2. What post-repair issues are typically excluded from a hardware repair warranty?\n"
                    "3. How do good job logs and final QA checks help both a small repair business and partner programs?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Power/Board Diagnostics & Shop Operations Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Laptop & PC Technician QR Certificate.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="A laptop shows charging/power lights and fan spin, but the built-in screen stays black. What is a smart first diagnostic step?",
            option_a="Test with an external monitor/display output and check RAM seating/power isolation before assuming a dead board",
            option_b="Immediately discard the laptop without checking display output or memory",
            option_c="Hammer the palmrest near the hinge",
            option_d="Plug in an unmatched high-voltage power supply",
            correct_answer="A",
            explanation="Checking external display output and memory/power basics isolates display vs. boot/board issues efficiently.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="Which approach best builds trust with customers and livelihood/institutional partners?",
            option_a="Clear upfront quotes, honest fault/risk communication, thorough post-repair QA, and clear warranty boundaries",
            option_b="Quoting vague numbers and adding surprise charges at pickup",
            option_c="Skipping post-repair testing to finish faster",
            option_d="Refusing to keep records of intake or completed work",
            correct_answer="A",
            explanation="Transparency, thorough QA, and clear terms build lasting trust and sustainable service operations.",
        )

        # =====================================================================
        # GLOSSARY TERMS (14 TERMS ACROSS TIER 1, TIER 2 & TIER 3)
        # =====================================================================
        glossary_items = [
            ("safety", "ESD", "Electrostatic Discharge", "Sudden transfer of static electricity that can harm sensitive electronics.", "Wear a grounded wrist strap on an ESD mat when handling internal components.", True, 1),
            ("general", "POST", "Power-On Self-Test", "Initial hardware check run when a computer powers on before OS loading.", "Helps distinguish early hardware/boot failures from OS-only issues.", True, 2),
            ("equipment", "BIOS / UEFI", "Basic Input/Output System / Unified Extensible Firmware Interface", "Low-level firmware controlling hardware initialization, boot order, and settings.", "Used to verify drives/RAM, set boot options, and check system status.", True, 3),
            ("equipment", "RAM", "Random Access Memory", "Fast temporary memory used by active programs and the operating system.", "Check capacity, generation/type, and proper slot seating during upgrades/faults.", True, 4),
            ("equipment", "NVMe / SATA SSD", "Non-Volatile Memory Express / Serial ATA Solid-State Drive", "Flash storage drives offering fast access and no moving platters.", "Match interface and form factor accurately when upgrading or replacing drives.", True, 5),
            ("equipment", "DC Jack / USB-C PD", "DC Power Connector / USB Power Delivery", "Power input port or negotiated charging standard supplying system power.", "Check physical integrity, fit, and proper voltage/wattage rating.", True, 6),
            ("equipment", "Thermal Paste", "Heat-Transfer Compound", "Thin conductive paste placed between a processor die and heatsink base.", "Clean old paste and apply a thin, even layer during cooling service.", False, 7),
            ("business", "Intake Check", "Pre-Repair Condition & Function Log", "Recording exterior condition, existing faults, and data risks before repair.", "Prevents blame for pre-existing issues and guides accurate quoting.", False, 8),
            ("equipment", "Hinge Assembly", "Lid Pivot & Mounting Bracket", "Mechanical joint linking the display lid to the base chassis.", "Inspect for stiffness or broken mounts so lid opening doesn't crack housings.", False, 9),
            ("business", "OS & Driver Setup", "Operating System & Device Driver Configuration", "Installing/recovering the OS and matching hardware drivers for full function.", "Ensures Wi-Fi, audio, display, trackpad, and ports work smoothly.", False, 10),
            ("safety", "Thermal Throttling", "Automatic Speed Reduction From High Heat", "Processor slowdown triggered to prevent overheating when cooling is restricted.", "Signals dust buildup, fan issues, or degraded thermal transfer.", False, 11),
            ("business", "Post-Repair QA", "Final Quality Assurance Check", "Testing power, charging, display, inputs, ports, and boot before handover.", "Catches loose connections or missed items before the client leaves.", False, 12),
            ("business", "Itemized Quote", "Clear Breakdown of Parts & Service", "Upfront pricing separating replacement parts, service/labor, and timeline.", "Builds trust and avoids billing surprises.", False, 13),
            ("business", "Warranty Scope", "Defined Repair Coverage & Exclusions", "Clear statement of what is covered vs. excluded (such as drops or spills).", "Protects both the customer and the repair workshop/partner hub.", False, 14),
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
                "Seeded Laptop & PC Hardware Repair across Tier 1, Tier 2, and Tier 3, "
                "including diagrams, reference tables, 14 glossary terms, and quizzes!"
            )
        )