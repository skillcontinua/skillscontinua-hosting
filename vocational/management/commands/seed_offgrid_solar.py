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
    help = (
        "Seeds the complete 3-tier Off-Grid Solar & Inverter Systems course, "
        "diagrams, reference tables, glossary, and assessments."
    )

    def handle(self, *args, **options):
        target_name = "Solar & Renewable Energy"
        target_description = (
            "Practical off-grid solar PV, battery storage, AC/DC protection, commissioning, "
            "and trade business operations designed for real-world field mastery."
        )

        category, _ = TradeCategory.objects.update_or_create(
            slug="solar-renewable-energy",
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
                    "Digital Clamp Multimeter (DC/AC Volts & Amps), Non-Contact Voltage Tester, "
                    "Measuring Tape & Laser/String Line, Compass / Sun-Path & Shading App, "
                    "Insulated Screwdriver Set, Site Audit & Load Worksheet, Safety Boots, Goggles & Gloves"
                ),
                "safety_guidelines": (
                    "1. Always isolate power and lock/tag out breakers before touching conductors or opening enclosures.\n"
                    "2. Treat solar panels as live DC voltage sources whenever exposed to daylight or work lights.\n"
                    "3. Remove metal rings, chains, and watches; inspect ladders and roofs before climbing."
                ),
                "field_tips_summary": (
                    "Never rely on guesswork for inverter or battery size—audit every appliance's "
                    "running watts, motor surge behavior, and daily hours, and map shading from 9:00 AM to 4:00 PM."
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
                    "- Inspect roofs, shading obstacles, cable paths, and equipment rooms before quoting.\n"
                    "- Identify structural, thermal, moisture, and electrical site hazards during a survey.\n"
                    "- Map shading windows between 9:00 AM and 4:00 PM and plan safe cable/equipment routing."
                ),
                "why_it_matters": (
                    "Missing afternoon shade or placing batteries in a hot, unventilated room ruins "
                    "system performance, triggers inverter faults, and shortens battery life from day one. "
                    "Accurate site audits protect both client satisfaction and technician profit margins."
                ),
                "core_explanation": (
                    "A reliable off-grid solar installation starts before any equipment is bought.\n"
                    "Even partial shading on a single panel in a series string can pull down the current "
                    "of the entire string and create localized hot spots.\n\n"
                    "SITE AUDIT REFERENCE MATRIX:\n"
                    "Check Area       | Key Standard / Inspection Point\n"
                    "-----------------+-------------------------------------------------------------\n"
                    "Sun & Shading    | Check 9AM, 12PM & 3-4PM for trees, tanks, walls & neighbors\n"
                    "Roof / Structure | Verify rafters/purlins, sheet condition, access & leaks\n"
                    "Equipment Room   | Cool, dry, shaded, ventilated; away from heat/fumes\n"
                    "Cable & Earthing | Short/clean PV & battery runs + accessible earth point"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Put on safety boots, protective eyewear, and high-visibility gear; inspect ladder rungs and feet on firm, level ground.\n\n"
                    "FIELD AUDIT STEPS:\n"
                    "1. Measure usable roof or ground footprint, tilt/orientation options, and structural support members.\n"
                    "2. Record shading objects and check how shadows move across the proposed array area between 9:00 AM and 4:00 PM.\n"
                    "3. Inspect the proposed inverter/battery location for airflow clearance, dry walls/floor, and distance from heat sources.\n"
                    "4. Measure approximate cable lengths from array to charge controller/inverter and from battery bank to inverter.\n"
                    "5. Note existing distribution board (DB) layout, heavy heating/motor circuits, and earthing conditions.\n\n"
                    "POST-AUDIT CHECK:\n"
                    "- Sketch a simple site layout showing array zone, cable route, equipment wall, and shaded/unshaded hours before preparing a quote."
                ),
                "safety_and_traps": (
                    "- TRAP (Fragile Roof Sheets & Glass): Never step on brittle roofing sheets, skylights, or solar module glass; bridge across structural supports or use proper staging.\n"
                    "- TRAP (Hot Inverter/Battery Closets): Mounting inverters and batteries inside sealed cupboards or direct afternoon sun causes thermal derating and early battery degradation.\n"
                    "- TRAP (Ignoring Future Obstacles): Young trees, unbuilt walls, or future water tanks near the array can create severe shade within months."
                ),
                "diagram_or_visual_guide": (
                    "[Roof / Array Zone] ===(DC PV Cables + SPD/MCB)===> [Cool, Shaded Equipment Room]\n"
                    "   - Check 9AM / 12PM / 3-4PM shadows               - Battery Bank <-> Inverter (short, thick leads)\n"
                    "   - Keep clear of chimneys/tanks/trees               - Essential AC Sub-DB <-> Heavy Loads separated"
                ),
                "real_life_scenario": (
                    "During a 10:30 AM site visit, a homeowner's roof looks completely clear. However, a tall "
                    "overhead water tank and neighbor's wall cast a shadow across the eastern edge of the roof by 2:00 PM. "
                    "By moving the array slightly west and keeping shaded zones clear, daytime battery charging stays strong through late afternoon."
                ),
                "practice_activity": (
                    "Perform a 20-minute site audit on a home, shop, or workshop: measure the available mounting area, "
                    "list every potential shading object and time of day it casts shade, pick an equipment location, "
                    "and estimate PV-to-inverter and battery-to-inverter cable distances."
                ),
                "checkpoint_questions": (
                    "1. Why can shading just one panel in a series string hurt the whole string's output?\n"
                    "2. What makes a room unsuitable for housing a battery bank and inverter?\n"
                    "3. Which three times of day should you pay special attention to when checking shade?"
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
                    "- Calculate running power (W) and daily energy demand (Wh/day and kWh/day) accurately.\n"
                    "- Distinguish continuous running load from motor/compressor startup surge.\n"
                    "- Apply a 20% system loss factor and flag high-wattage resistive heating loads."
                ),
                "why_it_matters": (
                    "Clients judge solar systems by whether their appliances run without tripping and whether "
                    "power lasts through the night. Underestimating Wh/day or ignoring surge loads leads to "
                    "inverter shutoffs, dead batteries, and costly system upgrades."
                ),
                "core_explanation": (
                    "Power (Watts, W) tells you how fast energy is used at a moment: W = V x A (or read from the appliance rating plate).\n"
                    "Energy (Watt-hours, Wh) tells you how much total energy is consumed over time: Wh = W x Hours.\n"
                    "1 kilowatt-hour (kWh) = 1,000 Wh.\n\n"
                    "LOAD AUDIT & SIZING FORMULA:\n"
                    "- Daily Load (Wh/day) = Sum of [Appliance Watts (W) x Daily Runtime Hours (h)]\n"
                    "- Effective Duty Cycle: Fridges/freezers cycle on and off; a fridge rated at 140W running 24h in a room might run ~8-12h equivalent per day depending on door openings and ambient heat.\n"
                    "- Surge Power: Compressors, pumps, and motors can draw 2x-5x running watts for a brief startup pulse.\n"
                    "- Adjusted Daily Energy (Wh/day) = Total Raw Wh/day x 1.20 (accounts for inverter/charging/wiring losses)."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Walk through every room and list actual appliance labels/stickers rather than guessing from memory.\n\n"
                    "LOAD AUDIT STEPS:\n"
                    "1. Record each appliance's rated Watts (or Volts x Amps) and note whether it is lighting, electronics, motor/compressor, or heating.\n"
                    "2. Estimate realistic daily hours of use (including effective compressor run hours for fridges/freezers).\n"
                    "3. Multiply Watts x Hours for each item to get Wh/day, then sum all items for Raw Daily Wh.\n"
                    "4. Multiply Raw Daily Wh by 1.20 to get Adjusted Daily Wh (and divide by 1,000 for kWh/day).\n"
                    "5. Separate high-draw heating appliances (electric irons, kettles, water heaters, space heaters, ovens) for special review.\n\n"
                    "POST-AUDIT CHECK:\n"
                    "- Review the list with the client to confirm weekend vs. weekday usage and nighttime vs. daytime loads."
                ),
                "safety_and_traps": (
                    "- TRAP (Confusing Running W with Wh): A 100W bulb on for 10 hours uses 1,000 Wh (1 kWh), while a 2,000W iron on for 0.5 hours (30 mins) also uses 1,000 Wh—but needs a much larger inverter capacity while running.\n"
                    "- TRAP (Unbudgeted Surge Loads): A refrigerator or freezer can trip a modest inverter at startup even when total running wattage looks low.\n"
                    "- TRAP (Hidden Heating Loads): Clients often plug kettles, irons, or heaters into backup sockets unless warned and separated."
                ),
                "diagram_or_visual_guide": (
                    "[Appliance Sticker: W or V x A] x [Hours/Day] = [Raw Wh/Day]\n"
                    "   + Identify Motor/Compressor Surge (x2-x5 brief startup)\n"
                    "   + Flag Heavy Heating Loads (High W, short bursts)\n"
                    "   x 1.20 System Loss Factor = [Adjusted Daily Wh/Day]"
                ),
                "real_life_scenario": (
                    "A client runs 6x 12W LED bulbs (7h = 504 Wh), 2x 70W fans (9h = 1,260 Wh), 1x 95W TV (5h = 475 Wh), "
                    "and 1x 140W fridge (10h effective = 1,400 Wh). Raw daily load = 3,639 Wh/day. Applying the 1.20 margin gives "
                    "~4,367 Wh/day (~4.37 kWh/day), with peak running load around ~497W if all run together plus fridge compressor surge."
                ),
                "practice_activity": (
                    "Calculate Raw Wh/day and Adjusted Wh/day (x 1.20) for: 8x 10W LEDs (6h), 1x 65W laptop/router setup (8h), "
                    "1x 120W TV + decoder (6h), and 1x 150W freezer (9h effective). Also identify which appliance has the highest startup surge."
                ),
                "checkpoint_questions": (
                    "1. What is the formula for daily energy in Watt-hours (Wh)?\n"
                    "2. Why do we multiply total daily Wh by 1.20?\n"
                    "3. Why does a freezer or fridge need extra surge headroom compared to an LED lamp?"
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
                    "- Read and explain essential electrical, solar PV, battery, and safety terms on site.\n"
                    "- Avoid costly specification mistakes when comparing panels, batteries, controllers, and breakers."
                ),
                "why_it_matters": (
                    "Solar datasheets and supplier quotes use standard abbreviations every day. "
                    "Mastering these terms early keeps you from buying incompatible parts or miscalculating runtime."
                ),
                "core_explanation": (
                    "CORE FIELD VOCABULARY:\n"
                    "- V (Volts) / A (Amps) / W (Watts): Electrical potential (pressure), current (flow rate), and power (rate of work).\n"
                    "- Wh / kWh: Watt-hour and kilowatt-hour—total energy used or stored.\n"
                    "- Ah (Amp-hour): Battery charge capacity rating at a specified nominal voltage (usable energy depends on voltage and DoD).\n"
                    "- Voc (Open-Circuit Voltage): Maximum voltage of a solar panel or string when no load is connected.\n"
                    "- MPPT (Maximum Power Point Tracking): Smart charge controller that tracks optimal voltage/current for maximum PV harvest.\n"
                    "- DoD (Depth of Discharge): Percentage of a battery's capacity discharged.\n"
                    "- SoC (State of Charge): Remaining charge percentage in a battery (0% to 100%).\n"
                    "- BMS (Battery Management System): Electronic protection/monitoring board inside lithium packs.\n"
                    "- MC4 / MCB / SPD / EPDM / GND: PV connector, circuit breaker, surge protection device, weatherproof rubber, and protective earth/ground."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Keep a pocket glossary or datasheet checklist handy whenever comparing equipment quotes.\n\n"
                    "TERMINOLOGY CHECK STEPS:\n"
                    "1. Check panel Voc and multiply by panels in series—compare against the MPPT controller's max PV input voltage.\n"
                    "2. Convert battery capacity to usable energy: Nominal Volts x Ah x Safe DoD.\n"
                    "3. Confirm breakers/SPDs match the circuit type (DC-rated for DC PV/battery, AC-rated for AC output/input).\n"
                    "4. Verify weatherproofing (EPDM seals, outdoor enclosure ratings) and grounding (GND) on every job.\n\n"
                    "POST-WORK CHECK:\n"
                    "- Use exact technical terms (Voc, Wh, Ah, DoD, MPPT, SPD, GND) in client quotes and handover notes."
                ),
                "safety_and_traps": (
                    "- TRAP (Assuming 100% Usable Ah): A 24V 200Ah battery holds 4,800 Wh nominal, not 4,800 Wh usable; safe DoD limits usable energy (~50% for lead-acid/tubular, ~80% for LiFePO4).\n"
                    "- TRAP (Ignoring Voc Rise in Cool Weather): Panel open-circuit voltage increases when temperatures drop—never push right up to the MPPT voltage ceiling.\n"
                    "- TRAP (AC Breaker on DC Circuit): DC arcs extinguish differently than AC arcs; always use properly rated DC protection on DC circuits."
                ),
                "diagram_or_visual_guide": (
                    "Usable Battery Energy (Wh) ≈ Battery Voltage (V) x Capacity (Ah) x Safe DoD (%)\n"
                    "Example (24V 200Ah @ 80% LiFePO4 DoD): 24 x 200 x 0.80 = 3,840 Wh usable."
                ),
                "real_life_scenario": (
                    "A client compares two 24V 200Ah battery options: a standard lead-acid/tubular bank (~50% safe DoD = ~2,400 Wh usable) "
                    "and a LiFePO4 battery (~80% safe DoD = ~3,840 Wh usable). Explaining usable Wh—not just Ah—helps the client pick the right runtime."
                ),
                "practice_activity": (
                    "Without looking at your notes, write the meaning and one field use for: Voc, DoD, MPPT, BMS, MC4, SPD, and EPDM."
                ),
                "checkpoint_questions": (
                    "1. Why is usable energy (Wh) more helpful than Ah alone when comparing batteries at different voltages or chemistries?\n"
                    "2. What does MPPT do on a solar charge controller?\n"
                    "3. Where is EPDM used on a solar installation?"
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
                    "All Tier 1 tools plus MC4 Crimper & Release Spanners, Wire Strippers & Cable Cutters, "
                    "Socket/Torque Wrench Set, EPDM Washers & Weather Sealant, DC MCB & DC SPD"
                ),
                "safety_guidelines": (
                    "1. Cover solar panels or keep strings open/insulated while cutting, stripping, or crimping.\n"
                    "2. Never exceed MPPT maximum PV input voltage (Voc with cold-weather margin).\n"
                    "3. Use DC-rated breakers on DC circuits and verify polarity + voltage with a multimeter before closing."
                ),
                "field_tips_summary": (
                    "Always verify series Voc against MPPT voltage limits and check polarity "
                    "with a multimeter before closing any DC breaker or connecting a charge controller."
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
                    "- Select appropriate system voltage (12V / 24V / 48V), cable gauge (mm²), and protective ratings.\n"
                    "- Prevent MPPT over-voltage and excessive DC/AC voltage drop."
                ),
                "why_it_matters": (
                    "Oversizing wastes client money, while undersizing causes voltage drop, overheating cables, "
                    "frequent inverter trips, and early battery replacement callbacks."
                ),
                "core_explanation": (
                    "SYSTEM SIZING FORMULAS & GUIDELINES:\n"
                    "- Battery Capacity (Ah) = (Adjusted Daily Wh x Autonomy Days) / (System Voltage V x Safe DoD)\n"
                    "- Solar Array (Wp) ≈ Adjusted Daily Wh / (Peak Sun Hours x Array/Charging Efficiency)\n"
                    "- Series String Voc = Number of Series Panels x Panel Voc (must stay below MPPT max Voc with margin)\n"
                    "- Parallel Strings Current = Number of Parallel Strings x Imp/Isc\n\n"
                    "SYSTEM VOLTAGE & CURRENT GUIDE:\n"
                    "DC Bus | Typical Load Scale      | Key Advantage\n"
                    "-------+-------------------------+--------------------------------------------\n"
                    "12V    | Small/entry loads       | Widely available 12V accessories/lamps\n"
                    "24V    | Medium home/office/shop | Half the DC current of 12V for same watts\n"
                    "48V    | Larger home/commercial  | Lower current & smaller cable/loss penalty"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Start with the verified Adjusted Daily Wh/day and list of simultaneous/surge appliances.\n\n"
                    "SIZING & SELECTION STEPS:\n"
                    "1. Choose system voltage (12V, 24V, or 48V) based on load size and future expansion.\n"
                    "2. Compute required battery Ah using safe DoD (~0.50 for lead-acid/tubular, ~0.80 for LiFePO4).\n"
                    "3. Size inverter continuous rating above simultaneous running load plus surge margin for motors/compressors.\n"
                    "4. Calculate required PV Wp and choose a series/parallel string layout whose Voc stays safely under the MPPT max rating.\n"
                    "5. Select cable cross-section (mm²) and DC/AC MCB/fuse ratings matched to current and cable run length.\n\n"
                    "POST-SIZING CHECK:\n"
                    "- Cross-check every component rating (Voc max, battery voltage, breaker current rating) on a single Bill of Materials (BoM)."
                ),
                "safety_and_traps": (
                    "- TRAP (Exceeding MPPT Max PV Voltage): Putting too many high-Voc panels in series can permanently damage the MPPT input stage.\n"
                    "- TRAP (Under-Sized Battery/Cable on High Surge): High surge current on a small battery or thin cable causes sharp voltage sag and low-voltage inverter shutdown.\n"
                    "- TRAP (AC Breaker on DC Circuit): Always verify DC voltage rating on solar/battery breakers."
                ),
                "diagram_or_visual_guide": (
                    "[Adjusted Wh/Day] ---> Battery Ah = (Wh x Days) / (V_sys x DoD)\n"
                    "[Peak Load + Surge] ---> Inverter Rating + Cable mm²\n"
                    "[Daily Wh + Sun Hrs] ---> Solar Wp ---> String Voc < MPPT V_max"
                ),
                "real_life_scenario": (
                    "Four 480W panels (each Voc = 49.5V) are planned for a 150V max MPPT controller. Wiring all 4 in series (4S) "
                    "would reach ~198V (and even higher in cold weather), exceeding the 150V controller limit. Wiring two series strings "
                    "of 2 panels in parallel (2S2P) keeps string Voc near ~99V—well within the 150V limit while doubling current capacity."
                ),
                "practice_activity": (
                    "Calculate the required 24V battery capacity (Ah) for 3,600 Wh/day adjusted load over 1 day of autonomy "
                    "using (a) 50% safe DoD and (b) 80% safe DoD."
                ),
                "checkpoint_questions": (
                    "1. How do you calculate required battery Ah from adjusted daily Wh, system voltage, and DoD?\n"
                    "2. Why is 4S risky on a 150V MPPT controller when each panel has Voc = 49.5V?\n"
                    "3. Why do higher-voltage DC banks (24V/48V vs. 12V) reduce cable current for the same wattage?"
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
                    "- Anchor mounting rails/brackets securely into structural members or solid bases.\n"
                    "- Prevent roof leaks using EPDM gaskets/washers, proper sealing, and wind uplift control.\n"
                    "- Position and torque panel clamps without stressing or cracking solar modules."
                ),
                "why_it_matters": (
                    "A leak around a single roof fastener can ruin ceilings and drywall, while weak anchoring "
                    "or improper clamping risks wind lift, panel micro-cracks, or falling equipment."
                ),
                "core_explanation": (
                    "MECHANICAL & WEATHERPROOFING STANDARDS:\n"
                    "- Structural Anchoring: Anchor roof brackets into structural rafters, purlins, or concrete/steel frames—never rely on thin sheet metal alone.\n"
                    "- Leak Prevention: Use EPDM rubber washers/gaskets and appropriate weather sealant at roof penetrations; inspect flashing/sealants carefully.\n"
                    "- Wind & Mechanical Load: Space rails and mid/end clamps within module manufacturer clamp zones and torque fasteners evenly.\n"
                    "- Clearance & Drainage: Maintain proper clearance above roofing/ground so rain runoff drains freely and air circulates under panels."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Confirm roof/ground access, safety harness/ladder setup, and structural member locations.\n\n"
                    "MOUNTING & SEALING STEPS:\n"
                    "1. Mark rail lines, bracket spacing, and clamp zones according to module/racking specifications.\n"
                    "2. Fasten brackets securely into structural members or bases using EPDM seals and weather sealant.\n"
                    "3. Align and level mounting rails; verify rail-to-bracket tightness.\n"
                    "4. Lift modules carefully onto rails, position mid/end clamps in approved zones, and tighten evenly.\n\n"
                    "POST-MOUNT CHECK:\n"
                    "- Verify no loose bolts, no crushed/cracked glass edges, and clean drainage/cable routing under the array."
                ),
                "safety_and_traps": (
                    "- TRAP (Fastening Only Into Sheet Metal): Thin roofing sheets can pull out under wind load or foot pressure—always anchor into structural framing or solid bases.\n"
                    "- TRAP (Clamping Outside Approved Zones): Clamping too close to corners or edges can stress module frames or cause glass micro-cracks.\n"
                    "- TRAP (Incomplete Weather Sealing): Skipping EPDM gaskets or leaving unsealed drill holes invites water leaks."
                ),
                "diagram_or_visual_guide": (
                    "[Structural Rafter / Purlin / Base] ---> [EPDM Seal + Bracket + Fastener]\n"
                    "                                                  |\n"
                    "                                                  v\n"
                    "                    [Aligned Rails] ---> [Approved Clamp Zones + Even Torque]"
                ),
                "real_life_scenario": (
                    "After a heavy windstorm and rain, a poorly fastened roof rail shifts and a fastener hole leaks "
                    "onto a bedroom ceiling. Anchoring into structural purlins with EPDM seals and checking clamp zones prevents both issues."
                ),
                "practice_activity": (
                    "List 5 mechanical and weatherproofing checks you will perform before and after mounting solar rails and panels."
                ),
                "checkpoint_questions": (
                    "1. Why anchor brackets into structural members rather than sheet metal alone?\n"
                    "2. What role do EPDM gaskets/seals play at roof penetrations?\n"
                    "3. Why follow manufacturer clamp zones when securing panels to rails?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=2,
            defaults={
                "title": "Step 6: DC Array Wiring, MC4 Crimping, Polarity Checks & DC MCB/SPD Protection",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Wire series, parallel, and series-parallel PV strings cleanly with proper strain relief.\n"
                    "- Crimp MC4 connectors reliably and verify DC polarity and open-circuit voltage with a multimeter.\n"
                    "- Wire DC isolators/MCBs and DC surge protective devices (SPDs) safely."
                ),
                "why_it_matters": (
                    "Reverse DC polarity or loose MC4 crimps cause arcing, melted connectors, and instant "
                    "damage to expensive charge controllers or inverters."
                ),
                "core_explanation": (
                    "DC PV WIRING & PROTECTION RULES:\n"
                    "- Polarity Discipline: Mark positive (+) red and negative (-) black/blue consistently, and measure polarity/voltage with a multimeter before connecting any controller.\n"
                    "- MC4 Quality: Strip insulation cleanly, crimp with the matching die so strands do not stray, and verify a firm mechanical click when mating connectors.\n"
                    "- DC Isolation & Surge Protection: Place accessible DC disconnect/MCB protection and DC SPD near the PV entry/controller on appropriate DC-rated hardware.\n\n"
                    "PRE-ENERGIZATION CHECKS:\n"
                    "Test Item       | Expected Field Result\n"
                    "----------------+-----------------------------------------------------\n"
                    "MC4 Crimp & Fit | Firm crimp, zero stray strands, positive click lock\n"
                    "DC Polarity     | (+) matches (+), (-) matches (-) at controller input\n"
                    "String Voltage  | Within MPPT max Voc rating (with safety margin)"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Keep PV strings open/unconnected while terminating, and set your multimeter to DC Volts.\n\n"
                    "DC WIRING STEPS:\n"
                    "1. Route PV cables cleanly away from sharp metal edges and high heat; secure with UV-rated ties/clips.\n"
                    "2. Strip conductor ends cleanly, crimp MC4 pins/sockets properly, and insert into housings until locked.\n"
                    "3. Measure string polarity and Voc at the array/isolator leads using a digital multimeter.\n"
                    "4. Wire DC MCB/isolator and DC SPD per diagram, keeping SPD leads short and direct.\n\n"
                    "POST-WIRING CHECK:\n"
                    "- Double-check polarity at the controller terminals with the breaker open before energizing."
                ),
                "safety_and_traps": (
                    "- TRAP (Reverse Polarity): Reversing (+) and (-) on a charge controller or inverter can blow input stages immediately.\n"
                    "- TRAP (Loose / Poor MC4 Crimps): High-resistance crimps overheat under PV current and can melt connector housings.\n"
                    "- TRAP (Long Tangled SPD Leads): Long, looping surge leads reduce surge clamping effectiveness."
                ),
                "diagram_or_visual_guide": (
                    "[PV String (+ / -)] ---> [Meter Polarity & Voc Check]\n"
                    "                            |\n"
                    "                            v\n"
                    "             [DC SPD + DC MCB Isolator] ---> [MPPT Charge Controller]"
                ),
                "real_life_scenario": (
                    "A new solar array produces zero charging current at noon. Checking the DC isolator input with a "
                    "multimeter shows reversed polarity on one extension pair—correcting the swap restores normal MPPT charging."
                ),
                "practice_activity": (
                    "Write out the exact multimeter checks you perform on a PV string before closing the DC breaker to the MPPT."
                ),
                "checkpoint_questions": (
                    "1. Why verify DC polarity and string voltage with a multimeter before connecting to an MPPT?\n"
                    "2. What happens if an MC4 crimp has high resistance or loose strands under load?\n"
                    "3. Why keep DC SPD connection leads short and direct?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Sizing, Mounting & DC Protection Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test your ability to size systems, mount safely, and wire DC/MC4/SPD protection.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="A charge controller is rated for a maximum PV input of 150V DC. Each solar panel has Voc = 48V. Why should you avoid putting 4 panels in series (4S)?",
            option_a="4 x 48V = 192V (plus higher voltage in cool weather), which exceeds the 150V limit and risks damage",
            option_b="Series wiring reduces voltage to zero",
            option_c="Four panels in series only work with AC appliances",
            option_d="150V controllers require at least 250V to start",
            correct_answer="A",
            explanation="Series voltages add up; exceeding maximum PV input voltage can damage the controller.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="What should you always do before closing the DC breaker that feeds a solar charge controller?",
            option_a="Verify polarity (+ and -) and string voltage with a multimeter",
            option_b="Guess polarity by wire color alone without measuring",
            option_c="Short (+) and (-) together at the breaker",
            option_d="Remove all fuses and breakers permanently",
            correct_answer="A",
            explanation="Measuring voltage and polarity prevents reverse-polarity damage and over-voltage surprises.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): COMMISSIONING, DIAGNOSTICS & BUSINESS / IOM READINESS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="off-grid-solar-tier-3-professional",
            defaults={
                "category": category,
                "title": "Off-Grid Solar & Inverter Systems — Tier 3: Commissioning, Faults & Business",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Commission inverters, batteries & AC distribution safely; "
                    "troubleshoot field faults systematically; quote profitably & deliver partner-ready "
                    "handover documentation for QR certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 10,
                "credential_awarded": "Tier 3 Master Off-Grid Solar Practitioner QR Certificate & Transcript",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus AC/DC Clamp Meter, Torque Driver/Wrench, "
                    "AC MCB / RCD / SPD Test Kit, Commissioning Checklist, Itemized Quote & Handover Log"
                ),
                "safety_guidelines": (
                    "1. Follow strict startup order: Battery bank & DC protection -> Charge controller/PV -> AC output & sub-DB loads.\n"
                    "2. Verify tight terminal torque, proper earthing/bonding, and RCD/MCB protection before applying full load.\n"
                    "3. Never leave exposed live conductors, unlabelled breakers, or undocumented settings at client handover."
                ),
                "field_tips_summary": (
                    "A clean handover pack—itemized quote/BoM, test readings, user guide, and maintenance "
                    "schedule—builds client trust and makes your work ready for institutional & livelihood partners."
                ),
                "course_glossary_overview": (
                    "Covers Commissioning Sequence, RCD / Earth Leakage, Voltage Drop, Thermal Derating, "
                    "Bill of Materials (BoM), Preventive Maintenance, and Handover Verification."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: System Commissioning, AC/DC Protection & Client Handover",
                "tier": "tier_3",
                "summary": "Bring systems online safely, verify AC/DC protection, and deliver complete documentation.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 7: Commissioning Sequence, Battery/Inverter Setup & AC Sub-DB Protection",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Execute a safe, repeatable startup and commissioning sequence for off-grid inverter systems.\n"
                    "- Configure battery parameters/limits appropriately and verify AC output & sub-DB protection.\n"
                    "- Record baseline voltage, current, and load test readings at handover."
                ),
                "why_it_matters": (
                    "Rushing startup or ignoring battery/AC settings can cause inverter overload trips, "
                    "overcharging/undercharging faults, or shock hazards on socket/lighting circuits."
                ),
                "core_explanation": (
                    "SAFE COMMISSIONING ORDER:\n"
                    "- Establish clean, tight battery connections and verify battery voltage before powering the inverter/controller.\n"
                    "- Configure battery chemistry/voltage/charging parameters accurately, then bring PV input online safely.\n"
                    "- Verify AC output voltage/frequency, test AC MCB/RCD protection, label circuits, and test loads progressively.\n\n"
                    "COMMISSIONING CHECKPOINTS:\n"
                    "Stage          | Key Verification\n"
                    "---------------+--------------------------------------------------------\n"
                    "Battery & DC   | Tight lugs, correct polarity & nominal voltage\n"
                    "PV & Charging  | Polarity/Voc checked; steady charging without fault codes\n"
                    "AC & Loads     | Clean AC output, breaker/RCD check & progressive load test"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Inspect all terminations for tightness, verify enclosures are closed, and confirm PPE is worn.\n\n"
                    "COMMISSIONING STEPS:\n"
                    "1. Confirm battery bank polarity, voltage, and DC protection, then connect battery to inverter/controller.\n"
                    "2. Configure battery type/charging limits and close PV DC isolator after verifying polarity and Voc.\n"
                    "3. Verify inverter AC output voltage/frequency and test AC distribution breakers/RCDs.\n"
                    "4. Switch on loads step by step (lighting -> electronics -> motor/fridge) while monitoring voltage and current.\n\n"
                    "POST-COMMISSIONING CHECK:\n"
                    "- Log measured battery V, PV V/A, and AC load readings on the commissioning sheet."
                ),
                "safety_and_traps": (
                    "- TRAP (Energizing Unchecked Loose Terminals): Loose high-current battery lugs heat up rapidly under load.\n"
                    "- TRAP (Dumping Full Load at Once): Turning on heavy/motor loads simultaneously can trigger avoidable startup trips.\n"
                    "- TRAP (Skipping Protection & Label Checks): Unlabelled breakers or untested trips create confusion during emergencies."
                ),
                "diagram_or_visual_guide": (
                    "[Battery Bank + DC MCB] ---> [Inverter / MPPT Setup] ---> [PV Array + DC SPD/MCB]\n"
                    "                                       |\n"
                    "                                       v\n"
                    "                      [AC Sub-DB: MCB/RCD] ---> [Step-by-Step Load Test]"
                ),
                "real_life_scenario": (
                    "A newly installed 3 kW off-grid system shuts down whenever a client switches on a fridge "
                    "plus lights and fans together. Commissioning in stages and reviewing peak/surge load behavior "
                    "prevents surprise trips and sets clear client operating habits."
                ),
                "practice_activity": (
                    "Create a 6-item commissioning checklist covering battery checks, PV checks, AC protection, and load testing."
                ),
                "checkpoint_questions": (
                    "1. Why verify battery connections and voltage before bringing PV and heavy AC loads online?\n"
                    "2. Why test AC loads progressively rather than switching everything on at once?\n"
                    "3. Why record baseline readings during commissioning?"
                ),
            },
        )

        mod5, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=2,
            defaults={
                "title": "Module 5: Fault Diagnostics, Maintenance & Trade / Partner Readiness",
                "tier": "tier_3",
                "summary": "Diagnose field faults cleanly, run preventive maintenance, and deliver credible quotes/handovers.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod5,
            order=1,
            defaults={
                "title": "Step 8: Systematic Solar Fault Diagnostics, Maintenance & Quoting / Handover",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Troubleshoot common off-grid faults (low charging, overload/low-battery trips, loose joints, shade).\n"
                    "- Build structured preventive maintenance routines and transparent, itemized quotes.\n"
                    "- Deliver clear client/partner handover documentation supporting livelihood & program accountability."
                ),
                "why_it_matters": (
                    "Long-term sustainability—for an independent technician, a community workshop, or an IOM/agency "
                    "livelihood program—depends on systems that stay running and clear records that prove value."
                ),
                "core_explanation": (
                    "STRUCTURED DIAGNOSTICS & COMMERCIAL DISCIPLINE:\n"
                    "- Fault Isolation: Check alarms/LEDs, measure actual DC/AC voltages and currents with a meter, inspect cable/lug tightness and shading, and isolate one subsystem at a time.\n"
                    "- Preventive Maintenance: Schedule periodic visual inspections of panels/mounts, terminals, ventilation, and battery/system health.\n"
                    "- Transparent Quoting & Handover: Separate equipment, mounting/cabling/protection BoS, and installation/commissioning labor, and leave a clear handover summary.\n\n"
                    "FAULT DIAGNOSTIC QUICK GUIDE:\n"
                    "Symptom                 | First Places to Inspect\n"
                    "------------------------+-----------------------------------------------------\n"
                    "Low / No PV Charging    | Shading, MC4/string connection, DC MCB, MPPT status\n"
                    "Frequent Inverter Trip  | Overload/surge demand, battery voltage sag, airflow\n"
                    "Hot Lug / Voltage Drop  | Loose terminal torque, undersized/long cable run"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Isolate unsafe circuits before touching terminals or opening enclosures.\n\n"
                    "DIAGNOSTICS & HANDOVER STEPS:\n"
                    "1. Note exact fault code/symptom and measure battery voltage, PV voltage/current, and AC load.\n"
                    "2. Inspect physical connections, shading, ventilation, and breaker states to pinpoint root cause.\n"
                    "3. Prepare itemized quotes showing BoM, installation scope, warranty/support terms, and maintenance options.\n"
                    "4. Complete handover walkthrough with client/partner and log final test readings.\n\n"
                    "POST-WORK CHECK:\n"
                    "- Confirm system runs stably after repair and file job/maintenance notes for repeat service."
                ),
                "safety_and_traps": (
                    "- TRAP (Replacing Parts Without Measuring): Swapping inverters or panels before checking voltage, polarity, or loose lugs wastes money.\n"
                    "- TRAP (Vague Lump-Sum Quotes): Unclear quotes cause disputes over extra cable, conduit, or mounting hardware.\n"
                    "- TRAP (Zero Handover Records): Leaving no operating summary or test record makes future maintenance harder."
                ),
                "diagram_or_visual_guide": (
                    "[Symptom / Alarm] ---> [Measure V & A + Visual Check] ---> [Isolate Root Cause]\n"
                    "                                                               |\n"
                    "                                                               v\n"
                    "                       [Clean Repair + Maintenance Log + Handover Pack]"
                ),
                "real_life_scenario": (
                    "A small clinic or livelihood workshop reports evening power cuts. Measuring battery voltage under load "
                    "and checking daily usage shows heavy daytime/evening loads draining the bank early—combining load "
                    "discipline, maintenance checks, and clear documentation restores reliable operation."
                ),
                "practice_activity": (
                    "Draft a 1-page job summary & handover template containing: site/load summary, key component specs, "
                    "measured startup readings, safety/care rules, and next maintenance check date."
                ),
                "checkpoint_questions": (
                    "1. Why measure voltages and currents before replacing a suspected faulty component?\n"
                    "2. What key categories should an itemized solar quote separate clearly?\n"
                    "3. How does good handover documentation support long-term sustainability?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Commissioning, Diagnostics & Business Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod5,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Off-Grid Solar Practitioner QR Certificate.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="An off-grid inverter keeps shutting down under load and a terminal lug feels noticeably warm during inspection. What should you check first?",
            option_a="De-energize safely, check terminal tightness/torque and cable sizing/condition, and verify load/battery state",
            option_b="Paint over the warm terminal lug with household paint",
            option_c="Bypass all breakers and fuses",
            option_d="Ignore the warm terminal if the lights still flicker on",
            correct_answer="A",
            explanation="Loose connections or undersized conductors create resistance heat and voltage drop under load.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="Why is providing an itemized quote and clear handover/maintenance record valuable for clients and institutional partners?",
            option_a="It creates transparency on scope and costs, supports safe operation, and enables ongoing maintenance",
            option_b="It guarantees zero maintenance is ever needed on any equipment",
            option_c="It replaces electrical safety rules",
            option_d="It is only required when dismantling a system",
            correct_answer="A",
            explanation="Clear documentation and itemized scope build trust, prevent disputes, and sustain long-term performance.",
        )

        # =====================================================================
        # GLOSSARY TERMS (18 TERMS ACROSS TIER 1, TIER 2 & TIER 3)
        # =====================================================================
        glossary_items = [
            ("general", "V (Volts)", "Electrical Potential Difference", "Measures electrical push/pressure driving current around a circuit.", "Check DC string/battery voltage and AC output voltage safely with a multimeter.", True, 1),
            ("general", "A (Amps)", "Ampere — Electric Current", "Measures the flow rate of electric charge through a conductor or device.", "Used to size cables, fuses, breakers, and clamp-meter current checks.", True, 2),
            ("general", "W (Watts)", "Electrical Power", "Rate of energy transfer or consumption (W = V x A for DC).", "Used to audit appliance loads and check inverter continuous/surge capacity.", True, 3),
            ("general", "Wh / kWh", "Watt-Hour / Kilowatt-Hour", "Measures total electrical energy consumed or stored over time (1 kWh = 1,000 Wh).", "Essential for daily load audits and sizing battery/PV energy balance.", True, 4),
            ("equipment", "Ah (Amp-Hour)", "Battery Charge Capacity Rating", "Indicates charge capacity at a specified nominal voltage over a rated discharge period.", "Multiply by nominal voltage and safe DoD to estimate usable Watt-hours.", True, 5),
            ("equipment", "Voc", "Open-Circuit Voltage", "Maximum voltage produced by a solar panel or series string when no load is drawn.", "Keep series string Voc (with temperature margin) below MPPT max input voltage.", True, 6),
            ("equipment", "MPPT", "Maximum Power Point Tracking", "Controller technology that tracks optimal voltage/current to maximize PV power harvest.", "Allows higher-voltage PV strings to charge lower-voltage battery banks efficiently.", True, 7),
            ("general", "DoD", "Depth of Discharge", "Percentage of a battery's rated capacity that has been discharged.", "Respecting safe DoD protects battery cycle life and usable energy estimates.", True, 8),
            ("general", "SoC", "State of Charge", "Remaining energy/charge level in a battery expressed as a percentage.", "Helps monitor charging progress and avoid deep discharge stress.", True, 9),
            ("equipment", "BMS", "Battery Management System", "Electronic circuit monitoring and protecting lithium battery cells/packs.", "Guards against over/under voltage, current spikes, and temperature extremes.", True, 10),
            ("equipment", "MC4", "Multi-Contact 4 mm PV Connector", "Standard weather-resistant plug/socket connector used on solar PV cables.", "Crimp cleanly with proper tooling and lock firmly to avoid heating/arcs.", False, 11),
            ("safety", "MCB", "Miniature Circuit Breaker", "Automatic switch that trips on overcurrent/short-circuit faults.", "Must match circuit voltage/current and DC vs. AC rating requirements.", False, 12),
            ("safety", "SPD", "Surge Protective Device", "Diverts transient voltage spikes/surges to protect sensitive equipment.", "Install with short, direct leads on PV DC and/or AC sides as specified.", False, 13),
            ("equipment", "EPDM", "Ethylene Propylene Diene Monomer", "Durable weather- and UV-resistant synthetic rubber used for seals and gaskets.", "Helps prevent water leaks at roof penetrations and outdoor enclosures.", False, 14),
            ("safety", "GND / Earthing", "Protective Grounding / Earth Bonding", "Connects exposed conductive frames/equipment to earth for safety and fault paths.", "Supports fault protection and surge/reference stability when properly installed.", False, 15),
            ("business", "BoM", "Bill of Materials", "Complete itemized list of equipment, cables, protection, mounts, and accessories.", "Prevents missing parts on site and keeps quotes clear and accurate.", False, 16),
            ("safety", "RCD", "Residual Current Device", "Protective device that trips on earth-leakage current to reduce shock risk.", "Supports personal protection on AC circuits alongside proper earthing.", False, 17),
            ("business", "Commissioning", "Structured Startup & Verification Process", "Step-by-step checks, settings, and load tests before handing a system over.", "Catches wiring/configuration issues early and documents baseline performance.", False, 18),
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
                "including diagrams, reference tables, 18 glossary terms, and quizzes!"
            )
        )