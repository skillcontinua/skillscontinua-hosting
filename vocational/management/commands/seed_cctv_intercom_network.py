# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_cctv_intercom_network.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from vocational.models import (
    TradeCategory,
    TradeCourse,
    TradeModule,
    TradeLesson,
    TradeGlossaryTerm,
)
from assessments.models import Quiz, Question


class Command(BaseCommand):
    help = "Seeds the complete 3-tier CCTV, Intercom & Network Installation course, glossary, and quizzes."

    def handle(self, *args, **options):
        target_slug = "cctv-intercom-network-installation"
        target_name = "CCTV, Intercom & Network Installation"
        target_description = (
            "Practical security camera (IP/PoE & analog HD), audio/video intercom, "
            "structured Cat6 cabling, router/switch setup, PoE budgeting, and fault diagnostics."
        )
        category = TradeCategory.objects.filter(
            Q(slug=target_slug) | Q(name=target_name)
        ).first()
        if category:
            category.slug = target_slug
            category.name = target_name
            category.description = target_description
            category.save()
        else:
            category = TradeCategory.objects.create(
                slug=target_slug,
                name=target_name,
                description=target_description,
            )

        # =====================================================================
        # TIER 1 (FREE): SITE SURVEY, CABLE TYPES & SECURITY/NETWORK BASICS
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="cctv-intercom-network-tier-1-foundation",
            defaults={
                "category": category,
                "title": "CCTV, Intercom & Network Installation — Tier 1: Site Survey & Cabling Basics",
                "description": (
                    "FREE TIER: Master camera blind-spot & height planning, intercom entry points, "
                    "Cat5e/Cat6 vs. RG59/power cable roles, safety at height, and core security/networking terms."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Security & Low-Voltage Cabling Readiness Record",
                "required_tools": (
                    "Ladder & Safety Harness/Spotter, Measuring Tape, Laser/Sightline Check, "
                    "Cable Stripper & Crimper, RJ45 Continuity / LAN Cable Tester, Multimeter"
                ),
                "safety_guidelines": (
                    "1. LADDER & HEIGHT SAFETY: Maintain three points of contact, lock ladder stance, and never overreach.\n"
                    "2. MAINS SEPARATION: Keep low-voltage network/intercom/CCTV runs safely separated from unshielded AC mains.\n"
                    "3. WEATHERPROOF JUNCTIONS: Never leave outdoor camera pigtails or RJ45 plugs exposed to rain/moisture."
                ),
                "field_tips_summary": (
                    "Walk the entry path, gates, parking lot, and cash counter with the client first—"
                    "a camera mounted too high for identification only shows the top of a hat."
                ),
                "course_glossary_overview": (
                    "Covers IP Camera vs. Analog HD (TVI/CVI/AHD), NVR vs. DVR, PoE (802.3af/at), "
                    "Cat5e / Cat6, T568A/T568B, RJ45, Intercom / Door Release, and Blind Spot."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Security Site Survey, Camera Angles & Cabling Foundations",
                "tier": "tier_1",
                "summary": "Map coverage zones, eliminate blind spots, and distinguish cabling/hardware roles.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: Security & Intercom Site Survey, Field of View & Blind-Spot Mapping",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Survey gates, entrances, corridors, and indoor/outdoor zones for CCTV and intercoms.\n"
                    "- Balance wide overview against face/plate clarity and avoid glare/backlighting traps."
                ),
                "why_it_matters": (
                    "Cameras aimed straight into bright afternoon sun or mounted 5 meters up on a wide wall "
                    "produce unusable silhouettes instead of clear evidence."
                ),
                "core_explanation": (
                    "Map choke points first: main gate, front door, reception/cashier desk, and stairwells. "
                    "Avoid pointing cameras directly into harsh sun or headlights, and place intercom outdoor "
                    "stations at accessible hand/voice height with indoor handsets/monitors where needed."
                ),
                "step_by_step_field_guide": (
                    "1. Walk perimeter, gates, doors, and interior high-value zones with the client.\n"
                    "2. Mark camera positions, mounting heights, and approximate cable paths to NVR/DVR/rack.\n"
                    "3. Check for sun glare, IR reflection off nearby walls/eaves, and tree growth.\n"
                    "4. Confirm intercom call/door-release wiring routes and power availability."
                ),
                "safety_and_traps": (
                    "TRAP: Mounting a camera right under an overhanging roof eave so infrared (IR) night light "
                    "bounces off the eave and blinds the lens at night."
                ),
                "real_life_scenario": (
                    "A shop's night camera turns pure white after dark because it sits 10 cm below a white "
                    "ceiling overhang—moving it slightly forward/down eliminates IR bounce."
                ),
                "practice_activity": (
                    "Sketch a site coverage map for a small home, shop, or compound showing 4 camera "
                    "positions, 1 intercom point, and cable routes."
                ),
                "checkpoint_questions": (
                    "1. Why does placing a camera too close under a bright overhang cause night-vision glare?\n"
                    "2. Which entry/activity zones should be prioritized on a security site survey?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Cat6 Structured Cabling, T568B Termination & Cable Testing",
                "estimated_minutes": 50,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Strip Cat6 jackets cleanly without nicking inner twisted pairs.\n"
                    "- Wire RJ45 connectors to T568B standard and verify all 8 conductors with a LAN tester."
                ),
                "why_it_matters": (
                    "One untwisted pair too long or one loose pin in an RJ45 plug causes intermittent "
                    "camera drops, slow speeds, or PoE failure."
                ),
                "core_explanation": (
                    "Keep twists right up to the connector entry (~13 mm / 0.5 in max untwist), arrange "
                    "wires in T568B order (White-Orange, Orange, White-Green, Blue, White-Blue, Green, "
                    "White-Brown, Brown), push all the way to the front of the RJ45 plug, crimp firmly, "
                    "and test pins 1–8."
                ),
                "step_by_step_field_guide": (
                    "1. Slide on strain boot if used, strip outer jacket cleanly without nicking copper.\n"
                    "2. Untwist, straighten, and order pairs in T568B sequence; trim evenly.\n"
                    "3. Seat wires fully into RJ45 plug, crimp with calibrated crimper, and verify with LAN tester."
                ),
                "safety_and_traps": (
                    "TRAP: Cutting into inner wire insulation while scoring the outer Cat6 jacket."
                ),
                "real_life_scenario": (
                    "An IP camera drops offline every few minutes; testing the patch cable reveals pin 3/6 "
                    "failing due to an incomplete crimp."
                ),
                "practice_activity": (
                    "Terminate both ends of a Cat6 patch/run cable using T568B and verify all 8 pins pass."
                ),
                "checkpoint_questions": (
                    "1. What is the standard T568B wire order starting from pin 1?\n"
                    "2. Why keep untwisted wire length near the RJ45 plug short?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 CCTV, Intercom & Cabling Readiness Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify security site survey, IR/glare awareness, and Cat6/RJ45 termination basics.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="A client's outdoor infrared camera works clearly during the day, but at night the image is washed out by bright white glare near the top. What is a common cause?",
            option_a="Infrared light reflecting off a nearby overhanging roof/wall/eave close to the lens",
            option_b="The RJ45 cable is too short",
            option_c="The monitor contrast is turned down to zero",
            option_d="The intercom handset is off the hook",
            correct_answer="A",
            explanation="Nearby surfaces in front of or directly above the lens reflect IR illumination back into the camera sensor.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="When terminating a standard Ethernet/IP-camera cable using T568B, what should you check before finalizing?",
            option_a="All 8 conductors are seated fully to the tip and verified with a cable tester",
            option_b="Only two wires are connected and the rest are left hanging",
            option_c="The outer jacket is stripped 15 cm back",
            option_d="No cable test is needed",
            correct_answer="A",
            explanation="Full seating and pin-to-pin continuity testing prevent intermittent links and PoE issues.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): CCTV/INTERCOM INSTALL, POE SWITCHES & LAN SETUP
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="cctv-intercom-network-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "CCTV, Intercom & Network Installation — Tier 2: Camera, Intercom & LAN Setup",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Mount and aim IP/analog cameras, wire audio/video "
                    "intercoms, size PoE switch power budgets, configure routers/switches/VLAN/Wi-Fi "
                    "APs, and set up NVR/DVR recording."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 14,
                "credential_awarded": "Tier 2 Security & Enterprise LAN Installation Certificate",
                "required_tools": (
                    "All Tier 1 tools plus Hammer Drill & Masonry/Wood Bits, PVC/EMT Conduit & Fittings, "
                    "Weatherproof Junction Boxes, PoE Switch / NVR / DVR, Laptop for IP/Router Configuration"
                ),
                "safety_guidelines": (
                    "1. DRILL & CONDUIT SAFETY: Check for hidden electrical/water lines before drilling walls and wear eye protection.\n"
                    "2. POE POWER BUDGET: Never exceed a PoE switch's total Wattage budget (especially with IR/PTZ cameras).\n"
                    "3. WATERPROOF JOINTS: Seal outdoor camera junction boxes and drip loops properly."
                ),
                "field_tips_summary": (
                    "Always add a 'drip loop' below outdoor entry points so rainwater runs off the lowest "
                    "point of the cable instead of tracking along the wire into a box or camera."
                ),
                "course_glossary_overview": (
                    "Covers PoE Budget (Watts), IP Addressing / DHCP / Static IP, SSID & Channel Planning, "
                    "NVR / DVR HDD Surveillance Rating, Drip Loop, and Intercom Call/Lock Relay."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: Camera & Intercom Mounting, Conduit Runs & PoE/NVR Setup",
                "tier": "tier_2",
                "summary": "Install clean, weatherproof camera and intercom systems with reliable recording.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: Mounting Cameras & Intercoms, Conduit/Drip Loops & NVR/PoE Setup",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Mount indoor/outdoor cameras and intercom stations cleanly with drip loops and junction boxes.\n"
                    "- Connect PoE/NVR/DVR hardware, format surveillance HDDs, and verify live feeds & recording."
                ),
                "why_it_matters": (
                    "Sloppy outdoor connectors and unformatted/standard desktop hard drives cause camera "
                    "blackouts and lost footage right when security video is needed most."
                ),
                "core_explanation": (
                    "Mount junction boxes cleanly, form a drip loop below outdoor entries, protect cables in "
                    "conduit/trunking where exposed, verify PoE switch wattage headroom, and initialize "
                    "surveillance-rated HDD storage in the NVR/DVR with continuous/motion recording."
                ),
                "step_by_step_field_guide": (
                    "1. Mark mounting holes, drill safely, and secure junction box & camera/intercom bracket.\n"
                    "2. Route cable with a drip loop and terminate/seal weatherproof connections.\n"
                    "3. Power up PoE switch/NVR/DVR, verify camera link & IP/video feed, and check storage recording."
                ),
                "safety_and_traps": (
                    "TRAP: Forgetting a drip loop on exterior cables—water follows the cable right into "
                    "the enclosure or connector."
                ),
                "real_life_scenario": (
                    "Six PoE cameras work until night IR turns on across all six, causing one camera to "
                    "reboot because the PoE switch wattage budget is maxed out."
                ),
                "practice_activity": (
                    "Outline a 5-point installation and recording check for a 4-camera + intercom job."
                ),
                "checkpoint_questions": (
                    "1. Why form a drip loop on exterior cables entering a building or junction box?\n"
                    "2. Why check total PoE wattage when multiple cameras switch on night IR?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: Local Area Networks (LAN), Routers, Switches & Wi-Fi Coverage",
                "tier": "tier_2",
                "summary": "Build clean home, office, and school networks with strong Wi-Fi and organized cabling.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 4: Router, Switch & Access Point Setup, IP Basics & Labelled Patching",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Wire routers, switches, and access points cleanly and verify DHCP/IP connectivity.\n"
                    "- Place Wi-Fi access points centrally and label cables/ports for easy maintenance."
                ),
                "why_it_matters": (
                    "Messy unlabelled patch panels and poorly placed access points turn simple office/school "
                    "networks into daily support headaches."
                ),
                "core_explanation": (
                    "Connect WAN/uplink ports properly, keep switches ventilated, place access points "
                    "elevated and clear of thick metal/concrete barriers where practical, use strong Wi-Fi "
                    "security (WPA2/WPA3), and label every drop clearly."
                ),
                "step_by_step_field_guide": (
                    "1. Inspect router/switch/AP hardware and plan clean rack/wall layout with airflow.\n"
                    "2. Connect uplinks and test wired speed/ping before tuning Wi-Fi placement.\n"
                    "3. Configure secure Wi-Fi credentials, guest/staff separation where needed, and cable labels."
                ),
                "safety_and_traps": (
                    "TRAP: Stacking heat-generating routers/switches inside closed metal/wooden boxes with zero airflow."
                ),
                "real_life_scenario": (
                    "A small office has strong Wi-Fi near the front desk but zero signal in the back room—"
                    "running a Cat6 drop to a ceiling/wall Access Point solves the dead zone cleanly."
                ),
                "practice_activity": (
                    "Map out a clean network layout (modem/router -> switch -> APs + wired drops) with "
                    "a cable-labeling convention."
                ),
                "checkpoint_questions": (
                    "1. Why is running a wired Cat6 link to an Access Point better than relying only on weak signal repeaters?\n"
                    "2. Why label cables and ports during installation?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 CCTV, Intercom & LAN Installation Proficiency Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test outdoor weatherproofing, PoE budgeting, NVR storage setup, and LAN/AP layout.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="Why do technicians form a 'drip loop' on an exterior cable just before it enters a wall or weatherproof junction box?",
            option_a="So water running down the cable drips off at the lowest point instead of entering the connection",
            option_b="To increase Ethernet speed to 100 Gbps",
            option_c="To replace the need for a circuit breaker",
            option_d="Because straight cables cannot carry video",
            correct_answer="A",
            explanation="A drip loop creates a low point where moisture sheds harmlessly rather than tracking into equipment.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="What happens if you place network switches and routers inside a completely sealed, unventilated cabinet?",
            option_a="Heat buildup can cause thermal throttling, random reboots, or shortened hardware lifespan",
            option_b="The Wi-Fi range automatically doubles",
            option_c="Power consumption drops to zero",
            option_d="Cable labels become permanent",
            correct_answer="A",
            explanation="Active networking hardware generates heat and needs ventilation to stay reliable.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): FAULT DIAGNOSTICS, SURGE/POWER & SITE CONTRACTS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="cctv-intercom-network-tier-3-professional",
            defaults={
                "category": category,
                "title": "CCTV, Intercom & Network Installation — Tier 3: Diagnostics, Surge & Contracts",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Troubleshoot intermittent links, camera dropouts, "
                    "intercom audio/buzz faults, and surge damage; protect systems with UPS/SPD/earthing; "
                    "quote commercial/residential jobs; and earn QR-verifiable certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 14,
                "credential_awarded": "Tier 3 Master Security & Network Integrator QR Certificate",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus LAN Cable Tester / Continuity Meter, "
                    "UPS / Surge Protection Strip / SPD, Labeling & Handover Documentation Kit"
                ),
                "safety_guidelines": (
                    "1. SURGE & POWER PROTECTION: Pair NVRs, switches, and network gear with UPS backup and surge protection.\n"
                    "2. SAFE FAULT ISOLATION: Test one segment at a time (patch cable -> switch port -> run -> camera) before replacing hardware.\n"
                    "3. SECURITY & PRIVACY ETHICS: Change default passwords immediately upon commissioning and respect client privacy."
                ),
                "field_tips_summary": (
                    "Leaving default admin passwords on cameras, NVRs, and routers is a major security risk—"
                    "always set strong credentials and hand over an organized system map at completion."
                ),
                "course_glossary_overview": (
                    "Covers UPS Backup, Surge Protection (SPD), Default Credential Hardening, "
                    "Link Flap / Packet Loss, Ground Loop / Audio Hum, and Maintenance SLA."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Fault Diagnostics, Surge/UPS Protection & Client Handover",
                "tier": "tier_3",
                "summary": "Resolve field faults systematically, harden security, and deliver turnkey handovers.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 5: Systematic CCTV, Intercom & Network Fault Troubleshooting",
                "estimated_minutes": 65,
                "learning_objectives": (
                    "- Isolate cable, port, power/PoE, and configuration faults step by step.\n"
                    "- Resolve intermittent drops, intercom noise/call issues, and no-recording faults."
                ),
                "why_it_matters": (
                    "Fast, methodical fault isolation saves hours on site and keeps commercial and "
                    "residential clients coming back to you for upgrades and maintenance."
                ),
                "core_explanation": (
                    "Test from the closest known-good point outward: swap a short known-good patch cord at "
                    "the switch/NVR, check link lights/PoE status, inspect cable damage or moisture in "
                    "junction boxes, and verify recording schedules and disk status."
                ),
                "step_by_step_field_guide": (
                    "1. Identify exact symptom (dead camera, intermittent drop, no intercom ring/audio, or no playback).\n"
                    "2. Test with a known-good patch cable and inspect port indicators/power supply.\n"
                    "3. Check outdoor terminations for water ingress, loose screws, or pinched cable.\n"
                    "4. Confirm NVR/DVR recording status, time sync, and client user access."
                ),
                "safety_and_traps": (
                    "TRAP: Replacing an expensive NVR or camera before testing the patch cord, port, or power adapter."
                ),
                "real_life_scenario": (
                    "One outdoor camera keeps going offline during rain—opening its junction box reveals "
                    "moisture entering a loose grommet; resealing and adding a drip loop resolves it permanently."
                ),
                "practice_activity": (
                    "Write a 4-step diagnostic checklist for an IP camera or network port showing 'No Link'."
                ),
                "checkpoint_questions": (
                    "1. Why test with a known-good short patch cable early during network/CCTV fault finding?\n"
                    "2. What should you inspect first if a camera drops out specifically during wet weather?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 6: Security Hardening, UPS/Surge Protection, Quoting & Maintenance Plans",
                "estimated_minutes": 55,
                "learning_objectives": (
                    "- Secure devices with strong passwords, UPS backup, and surge protection.\n"
                    "- Quote installations cleanly (equipment + cabling/BoS + labor + maintenance) and hand over documentation."
                ),
                "why_it_matters": (
                    "Power surges and un-itemized cable costs are two of the biggest threats to installer "
                    "profitability and client satisfaction."
                ),
                "core_explanation": (
                    "Protect NVRs, switches, and routers with UPS + surge protection against power cuts "
                    "and spikes, replace default passwords before handover, separate camera/network gear "
                    "from cable/conduit/labor on quotes, and offer quarterly checkups."
                ),
                "step_by_step_field_guide": (
                    "1. Change default passwords, set accurate date/time, and verify UPS runtime on NVR/router.\n"
                    "2. Present itemized quote covering hardware, cabling/conduit/boxes, and installation labor.\n"
                    "3. Deliver labeled cable/camera map, login handover sheet, and maintenance plan option."
                ),
                "safety_and_traps": (
                    "TRAP: Leaving factory default passwords active or under-quoting long cable/conduit runs."
                ),
                "real_life_scenario": (
                    "A brief power flicker restarts an un-backed-up NVR/router and misses a critical event—"
                    "adding a small UPS keeps recording and internet running seamlessly."
                ),
                "practice_activity": (
                    "Draft a handover checklist and quote outline for an 8-camera + Wi-Fi AP installation."
                ),
                "checkpoint_questions": (
                    "1. Why is adding a UPS to an NVR and main router/switch important?\n"
                    "2. Why change default device passwords before handing over a system?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Diagnostics, Hardening & Contracting Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 35,
                "instructions": "Capstone exam for Tier 3 Master Security & Network Integrator QR Certificate.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="An outdoor camera works fine in dry weather but loses signal after heavy rain. Which step addresses the most likely root cause?",
            option_a="Inspect the junction box/connector for moisture ingress, dry/clean it, reseal properly, and ensure a drip loop is in place",
            option_b="Increase screen brightness on the TV monitor",
            option_c="Disconnect the NVR hard drive",
            option_d="Remove the camera mount screws completely",
            correct_answer="A",
            explanation="Rainwater ingress at outdoor joints or missing drip loops commonly causes moisture-related signal loss.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="Before handing over a newly installed CCTV and Wi-Fi network to a client, what security practice should always be completed?",
            option_a="Change default factory passwords to strong credentials and document/hand over access cleanly",
            option_b="Leave default passwords unchanged and write them on the wall",
            option_c="Turn off recording completely",
            option_d="Leave cables unlabelled and disconnected",
            correct_answer="A",
            explanation="Changing default passwords protects cameras, NVRs, and routers from unauthorized access.",
        )

        # =====================================================================
        # GLOSSARY TERMS (AVAILABLE FROM TIER 1 & ACROSS ALL THREE TIERS)
        # =====================================================================
        glossary_items = [
            ("equipment", "PoE", "Power over Ethernet", "Delivers electrical power and network data over a single twisted-pair Ethernet cable.", "Check total PoE wattage budget so cameras/APs do not overload the switch.", True, 1),
            ("equipment", "NVR / DVR", "Network / Digital Video Recorder", "Recording unit that stores and manages video feeds from IP (NVR) or analog HD (DVR) cameras.", "Pair with surveillance-rated storage and verify recording schedules.", True, 2),
            ("tools", "Cat6 / RJ45", "Category 6 Twisted-Pair Cable & 8P8C Modular Plug", "Standard structured network/IP-camera cable and connector.", "Follow T568B order cleanly and test all 8 pins.", True, 3),
            ("safety", "Drip Loop", "Downward Cable Bend Prior to Entry Point", "Prevents water running along an outdoor cable from entering a box or camera.", "Form a gentle downward loop before entry points and seal openings.", True, 4),
            ("business", "UPS", "Uninterruptible Power Supply", "Battery backup unit keeping critical security and network gear online during outages.", "Protects NVRs, routers, and switches through brief power dips/outages.", False, 5),
            ("safety", "SPD", "Surge Protection Device", "Protects sensitive electronics against voltage spikes and transients.", "Helps prevent surge damage along power and exposed runs.", False, 6),
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
                "Seeded CCTV, Intercom & Network Installation across Tier 1, Tier 2, and Tier 3, "
                "including lessons, glossary terms, and quizzes!"
            )
        )