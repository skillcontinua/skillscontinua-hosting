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
    help = "Seeds the complete 3-tier Laptop & PC Hardware Repair course, glossary, and quizzes."

    def handle(self, *args, **options):
        category, _ = TradeCategory.objects.update_or_create(
            slug="laptop-pc-hardware-repair",
            defaults={
                "name": "Laptop & PC Hardware Repair",
                "description": (
                    "Dedicated laptop & computer hardware training covering ESD/internal battery "
                    "isolation, screw mapping, RAM/NVMe SSD upgrades, heatsink & thermal repasting, "
                    "hinge/keyboard/LCD panel replacement, DC/USB-C PD charging rails, and workshop ops."
                ),
            },
        )

        # =====================================================================
        # TIER 1 (FREE): SAFE LAPTOP TEARDOWN, SCREW MAPPING & POST DIAGNOSTICS
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-repair-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Laptop & PC Hardware Repair — Tier 1: Diagnostics, Screw Mapping & Safe Teardown",
                "description": (
                    "FREE TIER: Master laptop ESD safety, internal battery disconnection, screw-length "
                    "mapping, POST/beep/LED blink-code diagnostics, and core PC hardware terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Laptop Hardware Diagnostics Readiness Record",
                "required_tools": (
                    "Precision Screwdriver Set (PH0, PH1, Torx T5/T8), Nylon Pry Spudgers & Picks, "
                    "Compartmentalized Screw Tray / Magnetic Mat, ESD Wrist Strap, Digital Multimeter, "
                    "USB-C PD / Barrel Charger Tester, External HDMI/VGA Monitor"
                ),
                "safety_guidelines": (
                    "1. DISCONNECT CHARGER & INTERNAL BATTERY FIRST: Never unplug LCD/eDP or fan cables while battery is connected.\n"
                    "2. SCREW LENGTH DISCIPLINE: Never force a long case screw into a short motherboard standoff.\n"
                    "3. ESD & CAPACITOR CARE: Ground yourself before touching RAM sticks, SSDs, or motherboard chips."
                ),
                "field_tips_summary": (
                    "Always test a 'black screen' laptop on an external HDMI monitor first—if external "
                    "video works, the motherboard and GPU are alive and the fault is in the LCD panel, eDP cable, or backlight."
                ),
                "course_glossary_overview": (
                    "Covers POST, BIOS/UEFI, CMOS Battery, SODIMM RAM, NVMe M.2 SSD, SATA, "
                    "eDP Display Cable, Heatsink / Thermal Compound, USB-C PD, and VRM."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Laptop Triage, POST Codes & Non-Destructive Bottom-Case Teardown",
                "tier": "tier_1",
                "summary": "Isolate power/display/boot faults cleanly and open laptops without breaking clips or standoffs.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: No-Power vs. No-Display Triage, Blink Codes & External Monitor Test",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Separate dead-power issues from no-backlight/no-display faults in under 5 minutes.\n"
                    "- Read Caps-Lock/Power LED blink codes and external display output."
                ),
                "why_it_matters": (
                    "Clients often say 'my laptop won't turn on' when it is actually powering up with a "
                    "dead screen or loose RAM stick. Fast triage saves hours of guesswork."
                ),
                "core_explanation": (
                    "Check charger LED, fan spin, keyboard backlight, Caps-Lock LED blink patterns, and "
                    "external HDMI output. If external display works, focus on the LCD panel, hinge cable "
                    "(eDP), or backlight fuse. If Caps-Lock blinks a RAM error code, reseat/test SODIMM modules."
                ),
                "step_by_step_field_guide": (
                    "1. Inspect AC adapter/USB-C PD charger voltage and DC jack condition.\n"
                    "2. Press power and observe fan spin, LED blink patterns, and subtle screen backlight.\n"
                    "3. Connect an external HDMI monitor to verify motherboard video output.\n"
                    "4. Record intake condition, hinge cracks, and data backup notice."
                ),
                "safety_and_traps": (
                    "TRAP: Unplugging or plugging an eDP laptop screen cable while the battery is still "
                    "connected—this commonly blows the motherboard backlight fuse."
                ),
                "real_life_scenario": (
                    "A laptop powers on with fan noise and Caps-Lock response, and displays Windows on an "
                    "external TV via HDMI—proving the motherboard is healthy and isolating the fault to the display assembly."
                ),
                "practice_activity": (
                    "Run a 4-point intake diagnostic on a laptop: charger check, LED/fan check, flashlight "
                    "screen check, and external HDMI output test."
                ),
                "checkpoint_questions": (
                    "1. What does working video on an external HDMI monitor prove about a laptop?\n"
                    "2. Why must the internal battery be disconnected before touching the eDP display cable?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Screw-Length Mapping, Bottom-Cover Clips & Internal Battery Isolation",
                "estimated_minutes": 50,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Remove bottom covers (including screws hidden under rubber feet) without snapping plastic clips.\n"
                    "- Map screw lengths accurately and disconnect internal batteries safely."
                ),
                "why_it_matters": (
                    "Driving a long rear screw into a short front palmrest hole punches ugly dimples through "
                    "the palmrest or pierces motherboard traces."
                ),
                "core_explanation": (
                    "Many modern laptops hide screws beneath glued rubber strips/feet. Unscrew all perimeter "
                    "and center screws onto a mapped tray, slide a plastic pick along the seam starting near "
                    "the rear vents, and pull the battery connector straight out (or lift vertical locks) first."
                ),
                "step_by_step_field_guide": (
                    "1. Unplug charger and check beneath rubber feet for hidden base screws.\n"
                    "2. Place every screw in a position-matched tray.\n"
                    "3. Release bottom cover clips gently with a nylon spudger.\n"
                    "4. Disconnect internal battery connector and hold power button 5 seconds to drain residual charge."
                ),
                "safety_and_traps": (
                    "TRAP: Prying a metal screwdriver near the battery connector or pulling battery wires instead "
                    "of the plastic plug housing."
                ),
                "real_life_scenario": (
                    "A bottom cover refuses to lift at the center until you peel back the middle rubber foot "
                    "and find two hidden Phillips screws."
                ),
                "practice_activity": (
                    "Open a laptop bottom cover, map every screw by length/location, disconnect the battery, "
                    "and reassemble cleanly."
                ),
                "checkpoint_questions": (
                    "1. Where are hidden bottom-case screws often located on modern laptops?\n"
                    "2. Why hold the power button for 5 seconds after disconnecting the battery?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Laptop Safety, Triage & Teardown Readiness Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify laptop triage, external display testing, screw mapping, and battery isolation.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="A laptop turns on with fan spin, has a black built-in screen, but displays the desktop clearly on an external HDMI monitor. What does this tell you?",
            option_a="The CPU and GPU are working; inspect the built-in LCD panel, eDP cable, or backlight circuit",
            option_b="The hard drive is completely empty",
            option_c="The keyboard keys need lubrication",
            option_d="The laptop battery is overcharged",
            correct_answer="A",
            explanation="Clean HDMI output confirms core motherboard/GPU operation, narrowing the fault to the internal display path.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="Why is mapping laptop screw lengths during disassembly critical?",
            option_a="Long screws placed in short holes can pierce motherboard layers or push through the palmrest",
            option_b="All laptop screws are identical in every model",
            option_c="Screws conduct Wi-Fi signals",
            option_d="It makes the fan spin twice as fast",
            correct_answer="A",
            explanation="Laptop chassis use varying screw lengths; mixing them causes physical or electrical board damage.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): RAM/SSD UPGRADES, THERMAL SERVICING & PANEL/KEYBOARD SWAPS
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-repair-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Laptop & PC Hardware Repair — Tier 2: Upgrades, Thermal Servicing & Module Swaps",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Upgrade SODIMM RAM and NVMe/SATA SSDs, clean heatsinks "
                    "and repaste CPUs/GPUs, replace LCD panels, keyboards, fans, and DC jacks, and restore OS."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 14,
                "credential_awarded": "Tier 2 Laptop Servicing & Hardware Upgrade Certificate",
                "required_tools": (
                    "All Tier 1 tools plus Quality Thermal Paste & Thermal Pads, 99% Isopropyl Alcohol, "
                    "Anti-Static Brush / Blower, Soldering Iron & Flux (for DC jack/wire work), "
                    "Bootable Windows/Linux Diagnostic & OS Installation USB"
                ),
                "safety_guidelines": (
                    "1. HEATSINK TORQUE ORDER: Loosen and tighten heatsink screws in the numbered sequence (1-2-3-4) so bare CPU dies do not chip.\n"
                    "2. BATTERY DISCONNECTED FOR LCD WORK: Always disconnect battery + charger before swapping eDP screens.\n"
                    "3. DATA PROTECTION: Back up user partitions before cloning or reinstalling operating systems."
                ),
                "field_tips_summary": (
                    "Never wipe an old thermal pad off VRM chips unless replacing it with the exact same "
                    "thickness—using paste where a thick gap pad belongs leaves air gaps and overheats VRMs."
                ),
                "course_glossary_overview": (
                    "Covers DDR4/DDR5 SODIMM, M.2 NVMe vs. M.2 SATA Keying, Thermal Paste vs. Gap Pads, "
                    "30-Pin / 40-Pin eDP Panels, Keyboard Flex / Riveted Decks, and OS Cloning."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: RAM/SSD Upgrades, Thermal Repasting & Cooling System Restoration",
                "tier": "tier_2",
                "summary": "Speed up sluggish laptops and eliminate overheating shutdowns professionally.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: SODIMM RAM & NVMe/SATA SSD Upgrades + Clean OS Migration",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Match DDR generation, speed, and M.2 NVMe vs. SATA compatibility accurately.\n"
                    "- Clone or clean-install the OS and verify SMART drive health and dual-channel memory."
                ),
                "why_it_matters": (
                    "Upgrading a slow mechanical HDD to an NVMe/SATA SSD and expanding RAM is the fastest, "
                    "highest-satisfaction upgrade you can offer office and student clients."
                ),
                "core_explanation": (
                    "Check motherboard specs for DDR4 vs. DDR5 SODIMM support and M.2 PCIe NVMe vs. SATA "
                    "keying. Seat RAM at a ~30° angle until gold contacts disappear, then press down until "
                    "side clips click. Always verify drive health and back up user folders before migration."
                ),
                "step_by_step_field_guide": (
                    "1. Disconnect battery and verify supported RAM generation & M.2 slot type.\n"
                    "2. Install RAM/SSD firmly and secure the M.2 standoff screw.\n"
                    "3. Reconnect battery, confirm detection in BIOS/UEFI, and migrate/install OS & drivers."
                ),
                "safety_and_traps": (
                    "TRAP: Forcing DDR4 RAM into a DDR5 slot (notch positions differ) or leaving out the M.2 mounting screw."
                ),
                "real_life_scenario": (
                    "A client's office laptop takes 4 minutes to boot on an old HDD; migrating to an SSD and "
                    "adding a matching second RAM stick cuts boot time to under 15 seconds."
                ),
                "practice_activity": (
                    "Document the hardware compatibility check and BIOS verification steps for an SSD + RAM upgrade."
                ),
                "checkpoint_questions": (
                    "1. Why must you check M.2 NVMe vs. M.2 SATA compatibility before buying an upgrade drive?\n"
                    "2. What confirms a SODIMM RAM stick is properly seated?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=2,
            defaults={
                "title": "Step 4: Heatsink Cleaning, Numbered Torque Order & Thermal Repasting",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Remove dust mats blocking radiator fins and clean old thermal compound safely.\n"
                    "- Apply fresh paste and tighten heatsink screws in numbered order without chipping bare dies."
                ),
                "why_it_matters": (
                    "Clogged exhaust fins and dried factory paste cause thermal throttling, loud fans, and "
                    "eventual GPU/CPU solder failure."
                ),
                "core_explanation": (
                    "Hold fan blades still when blowing dust so overspinning does not damage bearings or "
                    "back-feed voltage. Clean old paste with 99% IPA, preserve VRM thermal pads, apply a "
                    "thin pea/line of quality thermal paste on the bare die, and tighten numbered heatsink "
                    "screws gradually in order."
                ),
                "step_by_step_field_guide": (
                    "1. Disconnect battery and unplug fan connector.\n"
                    "2. Loosen heatsink screws in reverse numbered order (4-3-2-1) and lift gently.\n"
                    "3. Clear lint mats between fan housing and copper fins; clean die & copper plate with 99% IPA.\n"
                    "4. Apply fresh thermal paste and tighten heatsink screws gradually in order (1-2-3-4)."
                ),
                "safety_and_traps": (
                    "TRAP: Cranking down screw #1 all the way before starting screws #2–#4—uneven pressure "
                    "can crack a bare silicon CPU/GPU die."
                ),
                "real_life_scenario": (
                    "A gaming/design laptop hits 98°C and shuts off mid-render; removing a thick felt lint "
                    "blockage inside the heatsink shroud and repasting drops load temps by 22°C."
                ),
                "practice_activity": (
                    "Perform a full fan/heatsink cleaning and thermal repaste on a practice laptop and log "
                    "idle vs. load temperatures before and after."
                ),
                "checkpoint_questions": (
                    "1. Why should heatsink screws be tightened gradually in numbered order?\n"
                    "2. Why should you hold the fan blades still while cleaning dust with compressed air?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: LCD Panel, DC-In Jack & Keyboard Replacement",
                "tier": "tier_2",
                "summary": "Replace cracked screens, loose charging ports, and liquid-spilled keyboards cleanly.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 5: 30/40-Pin eDP LCD Panel Replacement & DC-In Charging Port Repair",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Match exact LCD panel resolution, connector pin count (30-pin vs. 40-pin), and mounting brackets.\n"
                    "- Replace damaged barrel DC-in jacks and verify stable charging."
                ),
                "why_it_matters": (
                    "Installing a 40-pin touch/high-refresh cable onto a 30-pin panel (or leaving the battery "
                    "connected) destroys backlight circuits immediately."
                ),
                "core_explanation": (
                    "Disconnect the internal battery first, remove the bezel and stretch-release display "
                    "tape, match the exact LCD panel part number and pin count, test image/brightness before "
                    "snapping the bezel closed, and verify charging voltage/current at the motherboard."
                ),
                "step_by_step_field_guide": (
                    "1. Disconnect internal battery and remove LCD bezel carefully.\n"
                    "2. Release stretch-tape tabs/screws, flip panel forward, and unlatch eDP cable straight out.\n"
                    "3. Connect exact-match replacement panel, reconnect battery briefly to test display, then disconnect battery and reassemble bezel."
                ),
                "safety_and_traps": (
                    "TRAP: Forcing an eDP connector at an angle—bent pins short backlight power to data lines."
                ),
                "real_life_scenario": (
                    "A student brings a laptop with a cracked screen; matching the exact panel sticker code "
                    "and testing with battery isolated restores crystal-clear display."
                ),
                "practice_activity": (
                    "Write the verification checklist for ordering and installing a replacement laptop LCD panel."
                ),
                "checkpoint_questions": (
                    "1. What two specs must match when ordering a replacement laptop LCD panel?\n"
                    "2. Why align the eDP connector straight before latching it?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Laptop Upgrades, Thermal & Panel Servicing Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Verify RAM/SSD upgrades, thermal repasting discipline, and eDP LCD safety.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="Why must heatsink screws be tightened gradually in their numbered order (e.g., 1-2-3-4) when repasting a laptop CPU/GPU?",
            option_a="To apply even clamping pressure so the bare silicon die does not chip or crack",
            option_b="To disable the cooling fan during startup",
            option_c="To erase the BIOS password automatically",
            option_d="Because thermal paste only conducts when screw #1 is loose",
            correct_answer="A",
            explanation="Laptop CPUs/GPUs have exposed silicon dies; uneven torque can crack the die edge.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="What happens if you unplug or connect a laptop eDP display cable while the internal battery is still plugged in?",
            option_a="You risk blowing the motherboard's backlight fuse or damaging display lines",
            option_b="The SSD doubles in capacity",
            option_c="The keyboard layout changes language",
            option_d="Nothing electrical ever flows to the display connector",
            correct_answer="A",
            explanation="Standby battery voltage remains present on display power pins until the battery is disconnected.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): CHARGING RAILS, USB-C PD, HINGES & WORKSHOP OPS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="laptop-repair-tier-3-professional",
            defaults={
                "category": category,
                "title": "Laptop & PC Hardware Repair — Tier 3: Power Rails, Hinge/Chassis & Workshop Ops",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Trace 19V/20V USB-C PD and main power rails, diagnose "
                    "shorted MOSFETs/capacitors, rebuild broken laptop hinge brass standoffs, manage "
                    "corporate/school maintenance contracts, and earn QR-verifiable certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 16,
                "credential_awarded": "Tier 3 Master Laptop Technician QR Certificate & Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus Current-Limited DC Bench Power Supply, "
                    "USB-C PD Trigger/Analyzer, Digital Multimeter (Diode/Resistance/Voltage), "
                    "Hot-Air Rework Station, 2-Part Epoxy / Brass Threaded Inserts (for hinge repair)"
                ),
                "safety_guidelines": (
                    "1. CURRENT-LIMITED INJECTION: Limit voltage/current strictly when testing shorted 19V/20V or 3.3V/5V rails.\n"
                    "2. HINGE TENSION ADJUSTMENT: Slightly loosen overly stiff hinge nuts after rebuilding brass standoffs so plastic doesn't snap again.\n"
                    "3. CORPORATE DATA CONFIDENTIALITY: Enforce strict privacy and signed handover logs for business/school laptops."
                ),
                "field_tips_summary": (
                    "Rebuilding broken laptop hinge mounts with brass inserts + 2-part epoxy and slightly "
                    "loosening over-tight hinge friction nuts is a high-profit service almost every laptop owner needs."
                ),
                "course_glossary_overview": (
                    "Covers 19V/20V B+ Main Rail, USB-C PD Negotiation (5V to 20V), Input MOSFETs, "
                    "3.3V/5V Always-On Rails, EC / Super I/O, Brass Standoff Rebuild, and B2B Maintenance SLA."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Laptop Power-Rail Diagnostics, USB-C PD & Hinge Chassis Reconstruction",
                "tier": "tier_3",
                "summary": "Diagnose dead laptop motherboards and permanently repair broken hinge mounts.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 6: USB-C PD Negotiation, 19V Main Rail & Input MOSFET Diagnostics",
                "estimated_minutes": 70,
                "learning_objectives": (
                    "- Diagnose why a USB-C laptop stays stuck at 5V instead of negotiating 20V.\n"
                    "- Check input protection MOSFETs and main B+ power rail for shorts to ground."
                ),
                "why_it_matters": (
                    "Modern laptops rely on USB-C Power Delivery controllers and dual input MOSFETs—knowing "
                    "how to trace them turns 'dead motherboard' write-offs into profitable repairs."
                ),
                "core_explanation": (
                    "A healthy USB-C laptop negotiates from 5V up to 20V when connected to a PD charger. "
                    "If it stays at 5V with near-zero current, inspect the USB-C port pins, CC lines, and "
                    "PD controller. On barrel-jack laptops, measure voltage before and after the first and "
                    "second input MOSFETs and check the main B+ rail for a shorted filter capacitor."
                ),
                "step_by_step_field_guide": (
                    "1. Measure USB-C PD voltage/current negotiation (5V vs. 20V) or barrel adapter voltage.\n"
                    "2. Check main B+ power rail resistance/diode drop to ground before injecting power.\n"
                    "3. Isolate shorted input MOSFET or filter capacitor using current-limited bench testing.\n"
                    "4. Replace faulty component, clean flux, and verify battery charging + boot."
                ),
                "safety_and_traps": (
                    "TRAP: Injecting 19V directly onto a low-voltage CPU core rail—always verify rail "
                    "identity and limit injection voltage low first."
                ),
                "real_life_scenario": (
                    "A USB-C laptop refuses to charge and stays at 5.0V 0.02A; inspecting the port reveals "
                    "bent/corroded CC pins preventing 20V PD negotiation."
                ),
                "practice_activity": (
                    "Write the step-by-step diagnostic check when a USB-C laptop stays stuck at 5V."
                ),
                "checkpoint_questions": (
                    "1. What voltage should a healthy USB-C PD laptop charger negotiate from 5V?\n"
                    "2. Why check main B+ rail resistance to ground before applying full bench voltage?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 7: Permanent Hinge Standoff Reconstruction & Workshop / B2B Contracts",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Rebuild ripped-out brass hinge standoffs permanently and adjust hinge tension.\n"
                    "- Package recurring laptop servicing contracts for schools, offices, and cybercafes."
                ),
                "why_it_matters": (
                    "Broken laptop hinges are epidemic; fixing them permanently without replacing expensive "
                    "top covers plus securing institutional maintenance contracts builds steady income."
                ),
                "core_explanation": (
                    "Remove loose plastic debris, anchor brass threaded inserts cleanly in structural "
                    "2-part epoxy without getting epoxy inside screw threads or display cables, and back "
                    "off the hinge friction nut slightly so opening the lid doesn't rip the mount again."
                ),
                "step_by_step_field_guide": (
                    "1. Clean fractured plastic bosses and route LCD/Wi-Fi cables safely out of the hinge pocket.\n"
                    "2. Seat brass standoffs level in structural 2-part epoxy and allow full cure.\n"
                    "3. Slightly ease over-tight hinge friction nuts, reassemble, and test smooth lid motion.\n"
                    "4. Offer periodic preventive servicing (dust cleaning, repasting, SSD upgrades) to offices/schools."
                ),
                "safety_and_traps": (
                    "TRAP: Gluing over a stiff, seized hinge without easing its friction nut—the lid will "
                    "rip the repaired mount apart within weeks."
                ),
                "real_life_scenario": (
                    "A client's laptop lid separates at the right corner every time it opens; rebuilding the "
                    "brass inserts and easing hinge tension restores smooth, durable operation."
                ),
                "practice_activity": (
                    "Outline a 4-step hinge reconstruction procedure and a quarterly maintenance pitch for a local school or office."
                ),
                "checkpoint_questions": (
                    "1. Why should you slightly loosen overly stiff hinge nuts after rebuilding broken standoffs?\n"
                    "2. What services fit well into a quarterly school/office laptop maintenance contract?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Laptop Power-Rail & Workshop Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Laptop Technician QR Certificate & Transcript.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="A modern USB-C laptop refuses to charge and your USB-C tester shows it stays stuck at 5.0V instead of negotiating 20V. What is the most logical diagnostic path?",
            option_a="Inspect the USB-C port, CC communication pins, and PD controller negotiation path",
            option_b="Replace the laptop keyboard keys immediately",
            option_c="Tighten the hinge screws with pliers",
            option_d="Format the SSD to fix the USB-C voltage",
            correct_answer="A",
            explanation="USB-C Power Delivery requires healthy CC line communication between charger and PD controller to step up from 5V to 20V.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="After rebuilding ripped-out brass hinge standoffs with structural epoxy, what mechanical adjustment prevents the hinge from tearing the mount apart again?",
            option_a="Slightly loosen the overly stiff hinge friction nut so the lid opens smoothly",
            option_b="Glue the screen shut so the lid can never close",
            option_c="Pour epoxy directly into the cooling fan",
            option_d="Omit all hinge screws on one side",
            correct_answer="A",
            explanation="Excessive hinge friction is usually what tore the plastic bosses originally; easing the tension nut protects the repair.",
        )

        # =====================================================================
        # GLOSSARY TERMS (AVAILABLE FROM TIER 1 & ACROSS ALL THREE TIERS)
        # =====================================================================
        glossary_items = [
            ("general", "POST", "Power-On Self-Test", "Initial hardware check run by firmware immediately upon power-on.", "Beep or LED blink patterns diagnose RAM, CPU, or display faults.", True, 1),
            ("equipment", "SODIMM", "Small Outline Dual In-Line Memory Module", "Compact RAM module used in laptops.", "Match DDR generation (DDR4 vs. DDR5) and seat at 30° until side clips lock.", True, 2),
            ("equipment", "NVMe M.2", "Non-Volatile Memory Express M.2 SSD", "High-speed PCIe solid-state storage card.", "Verify NVMe vs. SATA slot keying before upgrading.", True, 3),
            ("equipment", "eDP", "Embedded DisplayPort", "Internal high-speed ribbon cable connecting motherboard to laptop LCD.", "Always disconnect the internal battery before unplugging or seating eDP.", True, 4),
            ("tools", "Thermal Paste", "Thermally Conductive Interface Compound", "Fills microscopic gaps between bare CPU/GPU die and copper heatsink.", "Clean old paste with 99% IPA and tighten heatsink screws in numbered order.", False, 5),
            ("equipment", "USB-C PD", "USB Type-C Power Delivery", "Smart charging protocol stepping voltage from 5V up to 20V.", "A laptop stuck at 5V indicates a port, CC line, or PD controller issue.", False, 6),
            ("equipment", "B+ Main Rail", "Primary 19V/20V System Power Rail", "Main power bus feeding laptop voltage regulators and charging circuits.", "Check resistance to ground before injecting power on dead boards.", False, 7),
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
                "including lessons, glossary terms, and quizzes!"
            )
        )