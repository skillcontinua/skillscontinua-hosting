# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_offgrid_solar.py
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
    help = "Seeds the complete 3-tier Off-Grid Solar & Inverter Systems course, glossary, and assessments."

    def handle(self, *args, **options):
        category, _ = TradeCategory.objects.update_or_create(
            slug="solar-renewable-energy",
            defaults={
                "name": "Solar & Renewable Energy",
                "description": (
                    "Practical off-grid solar PV, battery storage, AC/DC protection, commissioning, "
                    "and trade business operations designed for real-world field mastery."
                ),
            },
        )

        # =====================================================================
        # TIER 1 (FREE): FOUNDATION & SITE / LOAD AUDIT
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="off-grid-solar-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Off-Grid Solar & Inverter Systems — Tier 1: Foundation & Site Audit",
                "description": (
                    "FREE TIER: Build real confidence with electrical safety habits, essential field tools, "
                    "roof & shading audits, daily Watt-Hour (Wh) load math, and core solar terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Foundation Readiness Record",
                "required_tools": (
                    "Digital Clamp Multimeter, Measuring Tape, Compass/Sun-Path App, "
                    "Insulated Screwdriver Set, Site Audit Checklist, Safety Boots & Goggles"
                ),
                "safety_guidelines": (
                    "1. Always isolate power before touching conductors or opening enclosures.\n"
                    "2. Treat solar panels as live DC sources whenever exposed to daylight.\n"
                    "3. Remove metal jewelry and wear proper PPE and fall-safe ladder positioning."
                ),
                "field_tips_summary": (
                    "Never rely on guesswork for inverter or battery size—audit every appliance's "
                    "watts, surge behavior, and daily hours, and check shading from 9:00 AM to 4:00 PM."
                ),
                "course_glossary_overview": (
                    "Includes core electrical units (V, A, W, Wh, kWh, Ah), PV/MPPT terms "
                    "(Wp, Voc, MPPT, Series vs. Parallel), battery terms (DoD, SoC, BMS, LiFePO4), "
                    "and protection/mounting terms (MC4, MCB, SPD, EPDM, GND)."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Safety Culture, Site Assessment & Energy Load Auditing",
                "tier": "tier_1",
                "summary": "Site inspection, shading analysis, appliance load math, and starter field glossary.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: Site Audit, Shading Analysis & Hazard Assessment",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Inspect roofs, shading obstacles, and equipment rooms before quoting.\n"
                    "- Identify high-risk structural, thermal, and electrical site hazards."
                ),
                "why_it_matters": (
                    "Missing afternoon shade or placing batteries in a hot, unventilated room ruins "
                    "system performance and shortens battery life from day one."
                ),
                "core_explanation": (
                    "Map sun path and shadows between 9:00 AM and 4:00 PM. Even partial shading on "
                    "one panel in a series string limits string current. Place batteries and inverters "
                    "in cool, dry, ventilated indoor spots away from heat and moisture."
                ),
                "step_by_step_field_guide": (
                    "1. Check roof structure (rafters/purlins/slab) and available space.\n"
                    "2. Map shading obstructions from 9:00 AM to 4:00 PM.\n"
                    "3. Select a cool, dry, ventilated inverter/battery location and measure cable runs.\n"
                    "4. Note existing earthing and separate heavy heating/motor loads."
                ),
                "safety_and_traps": (
                    "TRAP: Never walk on fragile roofing sheets or solar glass without proper support "
                    "and fall protection."
                ),
                "real_life_scenario": (
                    "A water tank casts a 2:00 PM shadow over one panel on a roof. Moving or "
                    "re-stringing the array avoids crippling daytime charging."
                ),
                "practice_activity": (
                    "Conduct a site audit on one building: record roof dimensions, 9 AM–4 PM shadow "
                    "sources, equipment room location, and cable distance."
                ),
                "checkpoint_questions": (
                    "1. Why is afternoon shading critical during a site audit?\n"
                    "2. Why should batteries avoid hot, enclosed spaces?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Appliance Load Audit, Surge Power & Daily Watt-Hour (Wh) Math",
                "estimated_minutes": 50,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Calculate running power (W) and daily energy demand (Wh/day and kWh/day).\n"
                    "- Account for motor startup surge and apply a 20% system loss margin."
                ),
                "why_it_matters": (
                    "Accurate Wh/day math prevents under-sized battery banks and inverter overload trips."
                ),
                "core_explanation": (
                    "Watts (W) = Volts (V) x Amps (A). Daily Energy (Wh/day) = Watts x Hours/day. "
                    "Motors and compressors (fridges, freezers, pumps) draw surge power above running "
                    "watts at startup. Multiply total Wh/day by 1.20 to cover system losses."
                ),
                "step_by_step_field_guide": (
                    "1. List every client load and its rated wattage (W) and daily hours.\n"
                    "2. Estimate effective compressor duty hours for fridges/freezers.\n"
                    "3. Sum Wh/day across all loads and multiply by 1.20.\n"
                    "4. Flag high-draw heating loads (irons, kettles, heaters) clearly."
                ),
                "safety_and_traps": (
                    "TRAP: Confusing continuous running Watts with short-burst startup surge or "
                    "ignoring un-isolated high-wattage sockets."
                ),
                "real_life_scenario": (
                    "A small inverter trips whenever a fridge compressor starts despite lights and fans "
                    "being well within running wattage."
                ),
                "practice_activity": (
                    "Calculate total running Watts and Wh/day (plus 20% margin) for 6x 12W LEDs (7h), "
                    "2x 70W fans (9h), 1x 95W TV (5h), and 1x 140W fridge (10h effective)."
                ),
                "checkpoint_questions": (
                    "1. What is the difference between Watts (W) and Watt-Hours (Wh)?\n"
                    "2. Why do we multiply daily Wh by 1.20?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=3,
            defaults={
                "title": "Step 3: Tier 1 Field Glossary & Core Terminology Pocketbook",
                "estimated_minutes": 30,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Define key electrical, PV, battery, and safety acronyms used throughout the trade."
                ),
                "why_it_matters": (
                    "Knowing exact terms prevents misreading datasheets, buying wrong breakers, or "
                    "miscommunicating with clients and suppliers."
                ),
                "core_explanation": (
                    "V (Volts), A (Amps), W (Watts), Wh/kWh (Energy), Ah (Amp-hours), Voc (Open-Circuit "
                    "Voltage), MPPT (Maximum Power Point Tracking), DoD (Depth of Discharge), SoC "
                    "(State of Charge), BMS (Battery Management System), LiFePO4, MC4, MCB, SPD, EPDM, GND."
                ),
                "step_by_step_field_guide": (
                    "1. Check panel Voc against MPPT max input rating.\n"
                    "2. Multiply Battery V x Ah x safe DoD to estimate usable energy.\n"
                    "3. Use DC-rated breakers for DC circuits and AC-rated breakers for AC circuits."
                ),
                "safety_and_traps": (
                    "TRAP: Treating nominal Ah capacity as 100% usable energy on lead-acid/tubular "
                    "batteries without accounting for DoD."
                ),
                "real_life_scenario": (
                    "Comparing a 24V 200Ah tubular battery (~50% DoD) against a 24V 200Ah LiFePO4 "
                    "battery (~80% DoD) for nightly backup."
                ),
                "practice_activity": (
                    "Write definitions from memory for Voc, DoD, MPPT, MC4, SPD, and EPDM."
                ),
                "checkpoint_questions": (
                    "1. What does Voc represent?\n"
                    "2. What does EPDM do on a roof mount?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Readiness & Site/Load Audit Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Complete this Tier 1 check to verify site audit, load math, and starter term mastery.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="During a 2:00 PM site survey, a water tank casts a shadow over one solar panel in a series string. What is the best action?",
            option_a="Ignore it because a small shadow never affects string current",
            option_b="Eliminate/avoid the shading obstacle or configure strings so shaded panels do not choke the array",
            option_c="Replace the MPPT controller with a higher-wattage inverter only",
            option_d="Connect the shaded panel directly across the battery terminals",
            correct_answer="B",
            explanation="Shading a panel in a series string restricts current across the string and can cause localized heating.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="A 150W appliance runs for 6 hours per day. How much daily energy (Wh/day) does it consume before adding a loss margin?",
            option_a="25 Wh/day",
            option_b="156 Wh/day",
            option_c="900 Wh/day",
            option_d="1,500 Wh/day",
            correct_answer="C",
            explanation="Energy (Wh) = Power (150W) x Time (6 hours) = 900 Wh/day.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): SYSTEM SIZING, MOUNTING & DC PROTECTION
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="off-grid-solar-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Off-Grid Solar & Inverter Systems — Tier 2: System Sizing, Mounting & DC Wiring",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Size inverters, battery banks, solar arrays, cables, "
                    "and breakers; install weatherproof roof/ground mounts; crimp MC4 connectors and wire DC protection."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 10,
                "credential_awarded": "Tier 2 Practical Proficiency Certificate & Interim Transcript",
                "required_tools": (
                    "All Tier 1 tools plus MC4 Crimper & Release Spanners, Wire Strippers, "
                    "Socket/Torque Set, EPDM Washers & Sealant, DC MCB & SPD"
                ),
                "safety_guidelines": (
                    "1. Cover solar panels or keep strings open/insulated while terminating.\n"
                    "2. Never exceed MPPT maximum PV input voltage (Voc with cold-weather margin).\n"
                    "3. Use DC-rated breakers on DC circuits and verify polarity with a multimeter before closing."
                ),
                "field_tips_summary": (
                    "Always verify Voc in series strings against MPPT voltage limits and check polarity "
                    "with a multimeter before closing any DC breaker."
                ),
                "course_glossary_overview": (
                    "Covers Voc, Vmp, Isc, Imp, Series/Parallel/S-P topologies, MC4 crimping, "
                    "EPDM weatherproofing, wind uplift, and DC MCB/SPD protection."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: Inverter, Battery & Solar Array Sizing + Cable/Breaker Rules",
                "tier": "tier_2",
                "summary": "Translate Wh/day and surge load into balanced inverter, battery, PV, cable, and breaker specs.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 4: System Sizing (Inverter, Battery Ah/DoD, Solar Wp) & Cable/Breaker Selection",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Size inverter continuous + surge rating, battery Ah at safe DoD, and solar Wp.\n"
                    "- Select appropriate cable gauge (mm²) and breaker/fuse ratings to limit voltage drop."
                ),
                "why_it_matters": (
                    "Proper sizing prevents premature battery failure, over-voltage MPPT damage, and "
                    "overheating conductors."
                ),
                "core_explanation": (
                    "Battery Ah = (Adjusted Daily Wh x Autonomy Days) / (System Voltage V x Safe DoD). "
                    "Keep string Voc safely below MPPT max input voltage. Match cable cross-section (mm²) "
                    "to current and distance so voltage drop stays low."
                ),
                "step_by_step_field_guide": (
                    "1. Select system voltage (12V small, 24V medium, 48V larger loads).\n"
                    "2. Calculate required battery Ah using safe DoD (~50% lead-acid, ~80% LiFePO4).\n"
                    "3. Size solar array Wp for daily Wh and local peak sun hours.\n"
                    "4. Verify series string Voc against MPPT max voltage and size DC/AC protection."
                ),
                "safety_and_traps": (
                    "TRAP: Exceeding MPPT max PV voltage with too many panels in series, or using "
                    "AC-only breakers on DC circuits."
                ),
                "real_life_scenario": (
                    "Four 480W panels (Voc 49.5V each) are planned for a 150V max MPPT controller—4S "
                    "would approach/exceed safe voltage margin, whereas 2S2P stays near ~99V nominal."
                ),
                "practice_activity": (
                    "Size a 24V battery bank (Ah) for 3,600 Wh/day adjusted load at 50% usable DoD "
                    "with 1 day autonomy."
                ),
                "checkpoint_questions": (
                    "1. How do you convert required Watt-Hours into battery Amp-Hours (Ah)?\n"
                    "2. Why must series string Voc stay below the MPPT max voltage rating?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: Mechanical Mounting & DC Array / Protection Wiring",
                "tier": "tier_2",
                "summary": "Install rails/modules cleanly with waterproofing and wire strings, MC4s, DC MCBs, and SPDs.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 5: Roof & Ground Mounting Structures, Waterproofing & Wind Uplift Control",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Anchor mounting rails/brackets securely into structural members or bases.\n"
                    "- Prevent roof leaks using EPDM gaskets/washers and proper fastener torque."
                ),
                "why_it_matters": (
                    "Roof leaks destroy ceilings and electrical gear, while weak mounting risks wind damage."
                ),
                "core_explanation": (
                    "Fasten into structural rafters, purlins, or solid bases rather than thin sheet metal "
                    "alone. Use EPDM rubber seals and suitable weather sealant around penetrations, and "
                    "respect clamp zones and manufacturer torque limits."
                ),
                "step_by_step_field_guide": (
                    "1. Mark rail lines and clamp positions per manufacturer rules.\n"
                    "2. Anchor brackets to structural members with EPDM washers/sealing.\n"
                    "3. Mount rails level with expansion/airflow gaps.\n"
                    "4. Seat panels carefully and torque mid/end clamps evenly."
                ),
                "safety_and_traps": (
                    "TRAP: Over-tightening clamps and cracking tempered glass or walking on panels."
                ),
                "real_life_scenario": (
                    "A roof mount installed only into thin metal sheets loosens during strong gusts and "
                    "develops leaks around unsealed screw holes."
                ),
                "practice_activity": (
                    "List the mounting hardware, waterproofing seal steps, and clamp care rules for a "
                    "pitched roof installation."
                ),
                "checkpoint_questions": (
                    "1. Why fasten into structural members rather than thin roofing sheets alone?\n"
                    "2. What role does EPDM play at roof penetrations?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=2,
            defaults={
                "title": "Step 6: DC Array Wiring, MC4 Crimping & DC Protection (MCB / SPD)",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Wire series, parallel, and series-parallel strings and crimp reliable MC4 connectors.\n"
                    "- Verify string voltage and polarity with a multimeter before energizing DC protection."
                ),
                "why_it_matters": (
                    "Poor MC4 crimps cause hot spots and arcing, while reversed polarity can damage "
                    "expensive charge controllers."
                ),
                "core_explanation": (
                    "Series (+ to -) raises voltage; parallel (+ to +, - to -) raises current/capacity. "
                    "Crimp MC4 contacts firmly, click housings shut, and always check polarity and "
                    "voltage with a DC multimeter before closing DC MCB/isolator switches."
                ),
                "step_by_step_field_guide": (
                    "1. Cover panels or keep leads safe during cable routing.\n"
                    "2. Strip and crimp MC4 contacts cleanly; test pull firmness and lock.\n"
                    "3. Measure string Voc and polarity with a digital multimeter.\n"
                    "4. Wire DC isolator/MCB and DC SPD to earth and label polarity clearly."
                ),
                "safety_and_traps": (
                    "TRAP: Closing DC breakers or plugging into an MPPT before measuring polarity and "
                    "Voc with a multimeter."
                ),
                "real_life_scenario": (
                    "Two series strings of 45V each are paralleled (2S2P); you confirm ~90V string "
                    "voltage and exact +/- polarity at the DC isolator before switching on."
                ),
                "practice_activity": (
                    "Write out your exact pre-energization multimeter check and MC4 crimp verification steps."
                ),
                "checkpoint_questions": (
                    "1. What changes in series vs. parallel wiring?\n"
                    "2. Why must polarity be verified with a meter before closing DC breakers?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Practical Proficiency & Scenario Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "scenario_exam",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Demonstrate sizing, mounting, MC4/DC protection, and pre-energization safety mastery.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="You have four 480W panels (Voc = 49.5V each) and an MPPT controller with a 150V max PV input rating. Which configuration avoids risky over-voltage?",
            option_a="All 4 panels in series (4S, ~198V open-circuit)",
            option_b="Two series strings of 2 panels wired in parallel (2S2P, ~99V open-circuit)",
            option_c="Four panels in series with zero DC isolator",
            option_d="Connecting all positive leads to negative leads",
            correct_answer="B",
            explanation="4S (~198V) exceeds the 150V MPPT limit and risks permanent damage; 2S2P keeps voltage near ~99V while scaling current.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="Before closing a DC isolator connected to an MPPT charge controller, what should you verify with a multimeter?",
            option_a="Only AC frequency in Hertz",
            option_b="String voltage (Voc) and exact positive/negative polarity",
            option_c="Appliance power factor only",
            option_d="That the battery is disconnected",
            correct_answer="B",
            explanation="Measuring Voc and confirming +/- polarity prevents over-voltage or reverse-polarity damage.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): BATTERY/INVERTER, AC/EARTHING, COMMISSIONING & BUSINESS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="off-grid-solar-tier-3-professional",
            defaults={
                "category": category,
                "title": "Off-Grid Solar & Inverter Systems — Tier 3: Commissioning, Diagnostics & Business",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Integrate battery banks and inverters, configure charging "
                    "profiles, wire AC distribution & protective earthing, troubleshoot faults, quote clients, "
                    "and qualify for QR-verifiable certification & competency transcript."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 14,
                "credential_awarded": "Tier 3 Master QR Certificate & Full Competency Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus Hydraulic/Ratchet Lug Crimper, Heavy Copper "
                    "Battery Cables & Lugs, Earth Rod & Clamp, AC/DC MCBs & SPDs, Changeover Switch"
                ),
                "safety_guidelines": (
                    "1. Power up Battery FIRST, Solar PV SECOND, and AC loads LAST (reverse order on shutdown).\n"
                    "2. Use interlocked changeover switching so grid/generator never back-feeds inverter AC OUT.\n"
                    "3. Verify protective earthing (GND) and isolate faults safely before testing."
                ),
                "field_tips_summary": (
                    "Separate high-wattage heating loads from essential backup circuits, itemize BoS in "
                    "quotes, and shift heavy daytime loads to peak sun hours."
                ),
                "course_glossary_overview": (
                    "Covers Bulk/Absorption/Float/Low-DC cut-off, LiFePO4 vs. Lead-Acid, L-N-E & GND "
                    "earthing, changeover isolation, commissioning checks, fault diagnostics, and BoQ quoting."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Battery/Inverter Integration & AC Distribution / Earthing",
                "tier": "tier_3",
                "summary": "Configure charging parameters safely and build protected AC & earthing circuits.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 7: Battery Bank Interconnection, Inverter Integration & Charge Setup",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Wire balanced series/parallel battery banks and follow safe startup/shutdown order.\n"
                    "- Set Bulk, Absorption, Float, and Low-DC cut-off properly for Lead-Acid vs. LiFePO4."
                ),
                "why_it_matters": (
                    "Wrong voltage settings or startup sequence can damage batteries, BMS boards, or inverters."
                ),
                "core_explanation": (
                    "Match battery condition/voltage before paralleling, use balanced/diagonal connections "
                    "where applicable, configure chemistry-specific charging voltages (disabling equalization "
                    "on LiFePO4), and energize Battery first, PV second, AC loads last."
                ),
                "step_by_step_field_guide": (
                    "1. Inspect batteries and crimp heavy copper lugs cleanly.\n"
                    "2. Wire series/parallel connections and torque terminals safely.\n"
                    "3. Connect battery first so controller detects system voltage, then set parameters.\n"
                    "4. Connect PV second, then enable inverter and AC loads."
                ),
                "safety_and_traps": (
                    "TRAP: Connecting PV panels before the battery bank or leaving equalization enabled "
                    "on LiFePO4 packs."
                ),
                "real_life_scenario": (
                    "Configuring a 24V system for LiFePO4 vs. lead-acid/tubular batteries without "
                    "triggering premature BMS cutoff or overcharging."
                ),
                "practice_activity": (
                    "Write out the exact 4-step startup sequence and compare LiFePO4 vs. lead-acid "
                    "charging care rules."
                ),
                "checkpoint_questions": (
                    "1. Why does the battery bank power up before solar PV?\n"
                    "2. Why is equalization disabled on LiFePO4 batteries?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 8: AC Distribution, Changeover Isolation & Protective Earthing (L-N-E)",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Separate essential loads from heavy non-essential loads and prevent back-feeding.\n"
                    "- Install protective earthing (L, N, E / GND) and verify safe socket readings."
                ),
                "why_it_matters": (
                    "Prevents catastrophic back-feed inverter damage, electric shock, and surge harm."
                ),
                "core_explanation": (
                    "Keep heavy resistive/motor loads off backed-up circuits unless sized for them, use "
                    "interlocked changeover switching to block back-feed into inverter AC OUT, and bond "
                    "protective earth cleanly."
                ),
                "step_by_step_field_guide": (
                    "1. Route essential circuits to the backed-up sub-DB and exclude heavy loads.\n"
                    "2. Install AC MCBs, AC SPD, and interlocked changeover switching.\n"
                    "3. Drive and bond copper earth rod and verify L-N, L-E, and N-E readings."
                ),
                "safety_and_traps": (
                    "TRAP: Back-feeding utility grid or generator live voltage into inverter AC OUT."
                ),
                "real_life_scenario": (
                    "A makeshift changeover allows generator power to hit inverter AC OUT, blowing the "
                    "inverter output stage."
                ),
                "practice_activity": (
                    "Draw/outline an essential-load DB layout with AC MCB, SPD, changeover, and earth bond."
                ),
                "checkpoint_questions": (
                    "1. Why is back-feeding into inverter AC OUT dangerous?\n"
                    "2. Which appliances should stay off a small/medium backed-up load bus?"
                ),
            },
        )

        mod5, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=2,
            defaults={
                "title": "Module 5: Live Commissioning, Fault Diagnostics & Client Business Operations",
                "tier": "tier_3",
                "summary": "Commission systems systematically, troubleshoot faults, and build profitable trade operations.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod5,
            order=1,
            defaults={
                "title": "Step 9: Live Commissioning Protocol & Real-World Field Fault Diagnostics",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Execute a structured pre-handover commissioning check under real load.\n"
                    "- Diagnose startup voltage sag, 0A solar input, hot terminals, and grid input issues."
                ),
                "why_it_matters": (
                    "Systematic diagnostics turn stressful callbacks into fast, accurate fixes."
                ),
                "core_explanation": (
                    "Test mechanical/earth integrity, string Voc and charging current, transfer behavior, "
                    "and sustained load operation before handover. Diagnose faults by measuring actual "
                    "voltage/current at the point of failure rather than guessing."
                ),
                "step_by_step_field_guide": (
                    "1. Verify roof/mounting/earth integrity and log Voc, charging amps, and battery V.\n"
                    "2. Run essential loads for 15–20 minutes while checking for heat or alarms.\n"
                    "3. For faults, check battery sag under surge, PV Voc/MC4/MCB for 0A solar, and "
                    "lug crimps/tightness for hot spots."
                ),
                "safety_and_traps": (
                    "TRAP: Replacing parts blindly without measuring voltage under load or isolating "
                    "hot/damaged terminals first."
                ),
                "real_life_scenario": (
                    "An inverter runs evening lights fine but shuts down when a freezer starts, or shows "
                    "0W solar at midday."
                ),
                "practice_activity": (
                    "Write your troubleshooting steps for: (a) startup low-battery trip, and (b) 0A "
                    "solar charging at noon."
                ),
                "checkpoint_questions": (
                    "1. What do you measure when an inverter trips right as a motor/compressor starts?\n"
                    "2. How do you check whether a 0A solar reading starts at the roof or controller?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod5,
            order=2,
            defaults={
                "title": "Step 10: Client Handover, Maintenance Plans, BoQ Quoting & Self-Employment",
                "estimated_minutes": 50,
                "learning_objectives": (
                    "- Prepare clear itemized quotes (Core Equipment + BoS + Labor + Load Scope).\n"
                    "- Train clients on battery care, daytime solar usage, and preventive maintenance."
                ),
                "why_it_matters": (
                    "Transparent quoting protects profit margins, while client education prevents misuse "
                    "and builds recurring service revenue."
                ),
                "core_explanation": (
                    "Itemize major equipment, Balance of System (cables, MCBs, SPDs, mounts, earth rod), "
                    "and labor separately. Educate clients to run heavy loads during peak sun and "
                    "schedule periodic maintenance."
                ),
                "step_by_step_field_guide": (
                    "1. Present an itemized BoQ with clear included vs. excluded loads.\n"
                    "2. Train client on shutoff switches, alarms, SoC reading, and battery care.\n"
                    "3. Offer periodic maintenance checkups and display your verified QR credential."
                ),
                "safety_and_traps": (
                    "TRAP: Giving un-itemized lump-sum quotes that hide BoS costs or leaving clients "
                    "uninformed about high-wattage load limits."
                ),
                "real_life_scenario": (
                    "A client complains of short runtime after secretly plugging a high-wattage heater "
                    "into an essential socket; clear written load scope and handover training prevent disputes."
                ),
                "practice_activity": (
                    "Draft a sample 4-part quote outline (Equipment, BoS, Labor, Load/Care Scope) for a "
                    "home backup system."
                ),
                "checkpoint_questions": (
                    "1. Why separate BoS and labor from major equipment on a quote?\n"
                    "2. How does running daytime loads during peak sun help batteries?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Capstone Exam & Field Diagnostics",
            trade_course=tier3_course,
            trade_module=mod5,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone assessment required for Tier 3 Master QR Certificate & Competency Transcript eligibility.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="During commissioning, which power-up sequence protects voltage auto-detection and system stability?",
            option_a="Solar PV first, AC loads second, battery bank last",
            option_b="Battery bank first (configure settings), Solar PV second, AC loads last",
            option_c="AC grid back-feed first, then remove battery breaker",
            option_d="Close all DC and AC breakers simultaneously without checking polarity",
            correct_answer="B",
            explanation="Energizing the battery bank first establishes reference voltage and lets settings be configured before bringing in PV and AC loads.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="An inverter shuts down with a low-voltage alarm the instant a freezer compressor starts. What should you check?",
            option_a="Battery terminal voltage sag under startup surge and cable/lug resistance",
            option_b="Only the TV remote batteries",
            option_c="Whether the roof tiles are painted green",
            option_d="Turning off the system earth connection",
            correct_answer="A",
            explanation="Startup surge current can cause sharp voltage sag across weak battery banks or loose/undersized battery cables.",
        )

        # =====================================================================
        # GLOSSARY TERMS (AVAILABLE FROM TIER 1 & ACROSS COURSE)
        # =====================================================================
        glossary_items = [
            ("general", "Voc", "Open-Circuit Voltage", "Maximum voltage from a panel/string with no load connected.", "Must stay safely below MPPT max PV voltage limit.", True, 1),
            ("general", "Wh / kWh", "Watt-Hour / Kilowatt-Hour", "Energy used or stored over time (1 kWh = 1,000 Wh).", "Used to size daily loads and battery storage.", True, 2),
            ("equipment", "MPPT", "Maximum Power Point Tracking", "Charge controller tracking optimal voltage/current for max PV harvest.", "Generally higher yield than PWM when PV voltage exceeds battery voltage.", True, 3),
            ("equipment", "DoD", "Depth of Discharge", "Percentage of battery capacity discharged.", "Respect safe DoD (~50% lead-acid, ~80% LiFePO4) to protect battery life.", True, 4),
            ("equipment", "BMS", "Battery Management System", "Protection and monitoring electronics inside lithium packs.", "Monitors voltage, current, and temperature; set inverter cut-off above BMS trip.", True, 5),
            ("tools", "MC4", "Multi-Contact 4mm Connector", "Weather-resistant solar PV connector.", "Crimp cleanly and lock firmly to avoid resistance heating and arcing.", True, 6),
            ("safety", "EPDM", "Ethylene Propylene Diene Monomer", "Weather/UV-resistant synthetic rubber.", "Used in roof mounting washers/gaskets to prevent water leaks.", True, 7),
            ("safety", "SPD", "Surge Protection Device", "Diverts sudden voltage spikes toward earth.", "Protects DC and AC circuits against transient surges.", True, 8),
            ("safety", "GND", "Ground / Protective Earthing", "Connection of metal frames/chassis/surge paths to earth.", "Supports fault clearing, shock safety, and surge dissipation.", True, 9),
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
                "Seeded Off-Grid Solar & Inverter Systems across Tier 1, Tier 2, and Tier 3, "
                "including lessons, glossary terms, and quizzes!"
            )
        )