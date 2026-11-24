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
    help = (
        "Seeds the complete 3-tier CCTV, Intercom & Network Installation course, "
        "diagrams, reference tables, glossary, and quizzes."
    )

    def handle(self, *args, **options):
        target_slug = "cctv-intercom-network-installation"
        target_name = "CCTV, Intercom & Network Installation"
        target_description = (
            "Practical security camera (IP/PoE & analog HD), audio/video intercom, "
            "structured Cat6 cabling, router/switch setup, PoE budgeting, surge protection, "
            "and fault diagnostics."
        )

        category = TradeCategory.objects.filter(
            Q(slug=target_slug) | Q(name=target_name)
        ).first()
        if category:
            category.slug = target_slug
            category.name = target_name
            category.description = target_description
            if hasattr(category, "name_en"):
                category.name_en = target_name
            if hasattr(category, "description_en"):
                category.description_en = target_description
            category.save()
        else:
            create_kwargs = {
                "slug": target_slug,
                "name": target_name,
                "description": target_description,
            }
            if hasattr(TradeCategory, "name_en"):
                create_kwargs["name_en"] = target_name
            if hasattr(TradeCategory, "description_en"):
                create_kwargs["description_en"] = target_description
            category = TradeCategory.objects.create(**create_kwargs)

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
                    "Ladder & Safety Harness/Spotter, Measuring Tape, Sightline/Glare Check, "
                    "Cable Stripper & RJ45 Crimper, RJ45 Continuity / LAN Cable Tester, Digital Multimeter"
                ),
                "safety_guidelines": (
                    "1. LADDER & HEIGHT SAFETY: Maintain three points of contact, lock ladder stance, and never overreach.\n"
                    "2. MAINS SEPARATION: Keep low-voltage network/intercom/CCTV runs safely separated from unshielded AC mains.\n"
                    "3. WEATHERPROOF JUNCTIONS: Never leave outdoor camera pigtails or RJ45 plugs exposed to rain or moisture."
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
                    "- Balance wide overview against face/plate clarity and avoid glare/backlighting traps.\n"
                    "- Position outdoor intercom stations and indoor handsets/monitors for clear voice & access flow."
                ),
                "why_it_matters": (
                    "Cameras aimed straight into bright afternoon sun or mounted 5 meters up on a wide wall "
                    "produce unusable silhouettes instead of clear evidence—costing trust and repeat site visits."
                ),
                "core_explanation": (
                    "SURVEY PRIORITIES & COVERAGE ZONES:\n"
                    "- Choke Points First: Main gate, pedestrian entrance, reception/cashier counter, corridors, and equipment room.\n"
                    "- Glare & IR Bounce Control: Avoid pointing cameras directly into harsh sun or headlights, and keep lenses clear of close white overhangs/walls that reflect infrared (IR) light at night.\n"
                    "- Intercom Ergonomics: Place outdoor call stations at accessible reach/camera height and pair with indoor handsets/monitors or gate/door release wiring where requested.\n\n"
                    "CAMERA PLACEMENT QUICK REFERENCE:\n"
                    "Zone / Goal              | Typical Height   | Key Risk to Avoid\n"
                    "-----------------------+------------------+--------------------------------------\n"
                    "Front Door / Entry     | ~2.4 m - 3.0 m   | Overhead glare; angle slightly down\n"
                    "Cashier / Reception    | ~2.4 m - 3.0 m   | Backlit glass/window behind counter\n"
                    "Gate / Driveway        | ~2.8 m - 3.6 m   | Headlight glare; check night IR range\n"
                    "Intercom Call Station  | ~1.3 m - 1.5 m   | Direct rain exposure; noisy road spot"
                ),
                "step_by_step_field_guide": (
                    "PRE-SURVEY CHECK:\n"
                    "- Bring notepad/sketchpad, tape measure, flashlight, and a list of client security concerns.\n\n"
                    "SURVEY STEPS:\n"
                    "1. Walk perimeter, gates, doors, and interior high-value zones with the client.\n"
                    "2. Mark camera positions, approximate mounting heights, and cable routes to NVR/DVR/rack.\n"
                    "3. Check for sun glare, IR reflection off nearby walls/eaves, tree branches, and power points.\n"
                    "4. Confirm intercom call/door-release wiring routes and indoor station locations.\n\n"
                    "POST-SURVEY CHECK:\n"
                    "- Confirm every blind spot and client priority is logged before quoting materials."
                ),
                "safety_and_traps": (
                    "- TRAP (IR Bounce Under Eaves): Mounting a camera right under a bright overhanging eave causes IR night light to bounce back and wash out the image.\n"
                    "- TRAP (Height vs. Detail Tradeoff): Mounting too high gives a wide bird's-eye view but makes faces or details tiny.\n"
                    "- TRAP (Ignoring Future Growth): Trees, parked vehicles, or stacked goods can block a camera line of sight weeks later."
                ),
                "diagram_or_visual_guide": (
                    "[Street / Gate] ---> (Outdoor Intercom @ ~1.4m) ---> [Entry Choke Point @ ~2.7m]\n"
                    "                                                      |\n"
                    "      +-----------------------------------------------+ (Cat6 / Coax / Control)\n"
                    "      v\n"
                    "[NVR / DVR + PoE Switch + UPS Rack] ---> [Indoor Monitor / Client App]"
                ),
                "real_life_scenario": (
                    "A shop's night camera turns pure white after dark because it sits 10 cm below a white "
                    "ceiling overhang—moving it slightly forward/down eliminates IR bounce and restores clear night detail."
                ),
                "practice_activity": (
                    "Sketch a site coverage map for a small home, shop, or compound showing 4 camera "
                    "positions, 1 intercom point, and cable routes."
                ),
                "checkpoint_questions": (
                    "1. Why does placing a camera too close under a bright overhang cause night-vision glare?\n"
                    "2. Which entry/activity zones should be prioritized on a security site survey?\n"
                    "3. Why should you walk the site with the client before finalizing camera heights?"
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
                    "- Wire RJ45 connectors to T568B standard and verify all 8 conductors with a LAN tester.\n"
                    "- Compare Cat6, Cat5e, and coax/power cabling roles cleanly."
                ),
                "why_it_matters": (
                    "One untwisted pair too long or one loose pin in an RJ45 plug causes intermittent "
                    "camera drops, slow speeds, or PoE failure—turning a simple install into repeated callbacks."
                ),
                "core_explanation": (
                    "T568B PINOUT & TERMINATION DISCIPLINE:\n"
                    "- Keep pair twists right up to the connector entry (~13 mm / 0.5 in max untwist) to preserve noise rejection.\n"
                    "- Order conductors in T568B sequence (Pins 1-8): White-Orange, Orange, White-Green, Blue, White-Blue, Green, White-Brown, Brown.\n"
                    "- Push all 8 conductors all the way to the front tip of the RJ45 plug, check jacket grip inside the crimp collar, crimp firmly, and test pins 1-8.\n\n"
                    "T568B PINOUT QUICK TABLE:\n"
                    "Pin | Wire Color (T568B) | Typical Role\n"
                    "----+--------------------+---------------------------------\n"
                    " 1  | White-Orange       | TX+ / Data & PoE pair\n"
                    " 2  | Orange             | TX- / Data & PoE pair\n"
                    " 3  | White-Green        | RX+ / Data & PoE pair\n"
                    " 4  | Blue               | Pair / PoE pair (4-pair PoE)\n"
                    " 5  | White-Blue         | Pair / PoE pair (4-pair PoE)\n"
                    " 6  | Green              | RX- / Data & PoE pair\n"
                    " 7  | White-Brown        | Pair / PoE pair (4-pair PoE)\n"
                    " 8  | Brown              | Pair / PoE pair (4-pair PoE)"
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Inspect cable jacket for kinks/cuts and confirm your RJ45 tester battery is good.\n\n"
                    "TERMINATION STEPS:\n"
                    "1. Slide on strain boot if used, and strip outer Cat6 jacket cleanly without nicking copper/insulation.\n"
                    "2. Untwist, straighten, and arrange pairs in exact T568B order; trim wire ends flush/even.\n"
                    "3. Seat all 8 wires fully into the RJ45 plug, crimp with a calibrated crimper, and verify with a LAN cable tester.\n\n"
                    "POST-TEST CHECK:\n"
                    "- Confirm pins 1 through 8 pass in sequence with no open, short, or split-pair faults."
                ),
                "safety_and_traps": (
                    "- TRAP (Nickled Inner Conductors): Cutting into inner wire insulation while scoring the outer Cat6 jacket weakens copper and causes link faults.\n"
                    "- TRAP (Jacket Not Gripped by Crimp): Leaving the outer jacket outside the crimp bar lets tugs pull conductors out of the plug.\n"
                    "- TRAP (Skipping the Cable Tester): Assuming a crimp looks good visually without testing all 8 pins."
                ),
                "diagram_or_visual_guide": (
                    "[Cat6 Jacket] ---> [~13mm Max Untwist] ---> [T568B Order: WO-O-WG-Bl-WBl-G-WBr-Br]\n"
                    "                                       ---> [Full Tip Seat + Crimp + 1-8 Tester Pass]"
                ),
                "real_life_scenario": (
                    "An IP camera drops offline every few minutes; testing the patch cable reveals pin 3/6 "
                    "failing due to an incomplete crimp—re-terminating cleanly restores a rock-solid link."
                ),
                "practice_activity": (
                    "Terminate both ends of a Cat6 patch/run cable using T568B and verify all 8 pins pass."
                ),
                "checkpoint_questions": (
                    "1. What is the standard T568B wire order starting from pin 1?\n"
                    "2. Why keep untwisted wire length near the RJ45 plug short?\n"
                    "3. Why should you test every terminated cable with a LAN tester before installation?"
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
                    "intercoms, size PoE switch power budgets, configure routers/switches/Wi-Fi "
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
                    "- Connect PoE/NVR/DVR hardware, verify PoE wattage headroom, and initialize surveillance storage.\n"
                    "- Verify live feeds, intercom call/audio clarity, and continuous/motion recording."
                ),
                "why_it_matters": (
                    "Sloppy outdoor connectors and unformatted or standard desktop hard drives cause camera "
                    "blackouts and lost footage right when security video is needed most."
                ),
                "core_explanation": (
                    "WEATHERPROOFING, POE & STORAGE STANDARDS:\n"
                    "- Drip Loops & Enclosures: Form a downward drip loop below exterior cable entries and seal junction boxes/grommets so rain sheds cleanly.\n"
                    "- PoE Budget Margin: Sum camera wattage (including peak night IR and pan/tilt/zoom draw) and leave comfortable headroom below the switch's rated PoE budget.\n"
                    "- Surveillance Storage: Use surveillance-rated HDDs designed for 24/7 write cycles, initialize/format them in the NVR/DVR, and verify playback.\n\n"
                    "POE & STORAGE CHECKLIST:\n"
                    "Item                 | What to Verify\n"
                    "---------------------+------------------------------------------------\n"
                    "Exterior Entry       | Drip loop below entry + sealed junction/grommet\n"
                    "PoE Switch Budget    | Total camera watts (incl. night IR) <= Switch PoE W\n"
                    "Recorder Storage     | Drive detected, formatted cleanly, recording active"
                ),
                "step_by_step_field_guide": (
                    "PRE-INSTALL CHECK:\n"
                    "- Confirm wall/bracket anchors suit the surface and check PoE wattage and HDD capacity.\n\n"
                    "MOUNTING & SETUP STEPS:\n"
                    "1. Mark mounting holes, check for hidden utilities, drill safely, and secure junction box & camera/intercom bracket.\n"
                    "2. Route cable with a drip loop and terminate/seal weatherproof connections.\n"
                    "3. Power up PoE switch/NVR/DVR, verify camera link & IP/video feed, and initialize/verify recording.\n\n"
                    "POST-SETUP CHECK:\n"
                    "- Test both daylight and night/IR view plus intercom call/audio/release before closing up."
                ),
                "safety_and_traps": (
                    "- TRAP (Missing Drip Loop): Without a drip loop, rainwater tracks along the cable straight into the box or camera connector.\n"
                    "- TRAP (PoE Overload at Night): Cameras may run fine by day and reboot at night when IR LEDs draw extra power.\n"
                    "- TRAP (Assuming Recording Works Without Checking): Always verify disk status and playback rather than only viewing live feed."
                ),
                "diagram_or_visual_guide": (
                    "[Exterior Wall / Eave]\n"
                    "   |---> [Junction Box + Sealed Gland]\n"
                    "   |---> [Drip Loop v (Lowest Point Sheds Rain)] ---> [Indoor / Conduit Run]\n"
                    "                                                        |\n"
                    "                                                        v\n"
                    "                                              [PoE Switch / NVR + HDD]"
                ),
                "real_life_scenario": (
                    "Six PoE cameras work until night IR turns on across all six, causing one camera to "
                    "reboot because the PoE switch wattage budget is maxed out—moving a camera to a second "
                    "PoE switch or higher-budget switch fixes the drop."
                ),
                "practice_activity": (
                    "Outline a 5-point installation and recording check for a 4-camera + intercom job."
                ),
                "checkpoint_questions": (
                    "1. Why form a drip loop on exterior cables entering a building or junction box?\n"
                    "2. Why check total PoE wattage when multiple cameras switch on night IR?\n"
                    "3. Why verify recorded playback in addition to live camera view?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=2,
            defaults={
                "title": "Step 3B: Weatherproofing Outdoor Junctions, Audio/Video Intercom Wiring & Recording Verification",
                "estimated_minutes": 60,
                "is_free_preview": False,
                "learning_objectives": "- Seal outdoor camera and intercom junctions against rain, dust, and moisture ingress.\n- Wire intercom stations cleanly and verify continuous/event recording and playback before sign-off.",
                "why_it_matters": "Moisture entering outdoor connectors or unverified NVR recording schedules leads to blind spots and missed footage right when security incidents happen.",
                "core_explanation": "WEATHER SEALING & RECORDING VERIFICATION:\n- Protect exterior connections with drip loops, rated enclosures/glands, and proper sealing so water cannot wick into cables or terminals.\n- Confirm intercom voice/door-release operation and verify NVR storage retention, motion/schedule rules, and clock accuracy.\n\nFIELD SIGN-OFF BENCHMARK:\nCheck Area       | Verification Standard\n-----------------+--------------------------------------------------\nOutdoor Enclosures| Drip loop below entry + sealed glands/gaskets\nIntercom Station | Clear two-way audio/video + reliable door trigger\nRecorder & Clock | Active recording schedule + accurate date/time sync",
                "step_by_step_field_guide": "PRE-CHECK:\n- Confirm outdoor rating, cable slack/drip loop, and intercom call/unlock requirements.\n\nCOMMISSIONING STEPS:\n1. Form a drip loop below outdoor entry points and seal junction boxes/glands tightly.\n2. Terminate and test intercom indoor/outdoor stations for clarity and release response.\n3. Verify NVR/storage recording mode, retention days, and system time zone/clock.\n\nPOST-CHECK:\n- Play back test clips and confirm zero missed cameras or unrecorded channels.",
                "safety_and_traps": "- TRAP (Unsealed Cable Entry): Rainwater running along cable jackets enters enclosures and corrodes terminals.\n- TRAP (Assuming Default Recording): Leaving NVR channels on default or unscheduled settings can miss events.",
                "diagram_or_visual_guide": "[Outdoor Camera / Intercom] ---> [Drip Loop & Sealed Box] ---> [PoE Switch / NVR]\n                                                                        |\n                                       [Playback, Time Sync & Retention Check]",
                "real_life_scenario": "After heavy rain, an unsealed exterior junction box causes intermittent camera dropouts—sealing the enclosure and adding a proper drip loop restores steady operation.",
                "practice_activity": "Build a 6-point commissioning checklist covering outdoor weather sealing, intercom audio/door release, and NVR playback verification.",
                "checkpoint_questions": "1. Why is a drip loop below an exterior cable entry point important?\n2. What should you check on an NVR or recorder before handing over an installation?"
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
                    "NETWORK TOPOLOGY & CLEAN PATCHING:\n"
                    "- Connect WAN/uplink ports properly and verify IP addressing/DHCP lease and gateway reachability.\n"
                    "- Keep switches and routers ventilated away from enclosed heat traps.\n"
                    "- Place Wi-Fi access points elevated and clear of heavy metal/concrete dead zones, use strong Wi-Fi security (WPA2/WPA3), and label every cable drop and switch port clearly."
                ),
                "step_by_step_field_guide": (
                    "PRE-SETUP CHECK:\n"
                    "- Confirm router/switch/AP power bricks, patch cords, and cable label tags.\n\n"
                    "NETWORK SETUP STEPS:\n"
                    "1. Inspect router/switch/AP hardware and plan clean rack/wall layout with airflow.\n"
                    "2. Connect uplinks and test wired speed/ping before tuning Wi-Fi placement.\n"
                    "3. Configure secure Wi-Fi credentials, guest/staff separation where needed, and clear cable labels.\n\n"
                    "POST-SETUP CHECK:\n"
                    "- Verify both wired LAN devices and wireless clients connect reliably without IP conflicts."
                ),
                "safety_and_traps": (
                    "- TRAP (Sealed Heat Enclosures): Stacking heat-generating routers/switches inside closed boxes causes thermal throttling or reboots.\n"
                    "- TRAP (Unlabelled Spaghetti Drops): Guessing which cable goes to which room wastes hours during troubleshooting.\n"
                    "- TRAP (Weak/Default Wi-Fi Security): Leaving open or weak Wi-Fi credentials exposes client networks."
                ),
                "diagram_or_visual_guide": (
                    "[ISP / Modem / Router] ---> [Managed/Unmanaged Switch] ---> [Labelled Wired Drops]\n"
                    "                                           |--------------> [Ceiling/Wall Wi-Fi APs]"
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

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=2,
            defaults={
                "title": "Step 4B: VLAN/Subnet Segmentation, Wi-Fi Channel Planning & Rack/Patch Documentation",
                "estimated_minutes": 55,
                "is_free_preview": False,
                "learning_objectives": "- Separate security/IoT traffic from general user traffic using clean IP/VLAN boundaries.\n- Plan non-overlapping Wi-Fi channels and document patch panels, switch ports, and IP assignments.",
                "why_it_matters": "Unplanned Wi-Fi channels cause interference and slow throughput, while undocumented switch ports turn future troubleshooting into guesswork.",
                "core_explanation": "SEGMENTATION, WI-FI & DOCUMENTATION:\n- Keep camera/intercom/management addresses organized and separate from untrusted guest or general traffic where supported.\n- Assign non-overlapping channels and sensible placement for access points, and keep a clear port/IP/label record.\n\nNETWORK HYGIENE MATRIX:\nLayer          | Clean Standard\n---------------+--------------------------------------------------\nIP & Segments  | Documented static/DHCP ranges + isolated IoT/cam path\nWireless APs   | Non-overlapping channels + tested coverage at target zones\nPatch & Labels | Matching cable/port labels + accurate port map",
                "step_by_step_field_guide": "PRE-CHECK:\n- Map connected devices (NVRs, cameras, intercoms, APs, PCs) and note static vs. DHCP roles.\n\nCONFIGURATION STEPS:\n1. Verify IP addressing, gateway, and subnet consistency across switches, APs, and devices.\n2. Configure non-overlapping Wi-Fi channels and check signal strength in key rooms.\n3. Label patch panel/switch ports and record device names, MAC/IP details, and locations.\n\nPOST-CHECK:\n- Test connectivity across wired and wireless segments and save the port/IP map.",
                "safety_and_traps": "- TRAP (Duplicate Static IPs): Two devices sharing a static IP cause intermittent drops and conflicts.\n- TRAP (Unlabelled Patch Cables): Guessing port mappings later wastes hours during faults or upgrades.",
                "diagram_or_visual_guide": "[Router / Gateway] ---> [Managed/PoE Switch] ---> [Labels & Port/IP Map]\n                                    |---> [Camera / Intercom Segment]\n                                    |---> [Tuned Wi-Fi Access Points]",
                "real_life_scenario": "Two nearby access points on overlapping channels slow down video streams—assigning clean channels and documenting switch ports stabilizes throughput.",
                "practice_activity": "Draft a sample switch-port and IP allocation table for 6 network/security devices plus 2 access points.",
                "checkpoint_questions": "1. What problem occurs when two network devices are assigned the same static IP address?\n2. Why document switch ports and cable labels at installation time?"
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
                    "SEGMENTED FAULT ISOLATION:\n"
                    "- Isolate one segment at a time from known-good gear outward: short test patch cord -> switch/NVR port -> horizontal/outdoor cable run -> camera/intercom unit.\n"
                    "- Check link LEDs, PoE power status, cable continuity/pinout, outdoor junction boxes for moisture/corrosion, and NVR/DVR disk & recording schedules.\n\n"
                    "SYMPTOM-TO-CHECK MATRIX:\n"
                    "Symptom                   | First Segment to Check\n"
                    "--------------------------+------------------------------------------------\n"
                    "Camera / Link Offline     | Patch cord, switch/NVR port & PoE status, cable\n"
                    "Rain-Triggered Dropout    | Outdoor junction box, grommets, drip loop\n"
                    "Intercom Buzz / No Audio  | Wire polarity/continuity, power supply, hum/noise\n"
                    "Missing / Old Recordings  | HDD health/format, retention/motion schedule"
                ),
                "step_by_step_field_guide": (
                    "PRE-DIAGNOSIS CHECK:\n"
                    "- Note exact fault symptoms and when they occur (constant, during rain, or at night).\n\n"
                    "TROUBLESHOOTING STEPS:\n"
                    "1. Identify exact symptom (dead camera, intermittent drop, no intercom ring/audio, or no playback).\n"
                    "2. Test with a known-good patch cable and inspect port indicators/power supply.\n"
                    "3. Check outdoor terminations for water ingress, loose screws, or pinched cable.\n"
                    "4. Confirm NVR/DVR recording status, time sync, and client user access.\n\n"
                    "POST-FIX CHECK:\n"
                    "- Run a sustained observation check so intermittent drops do not return right after you leave."
                ),
                "safety_and_traps": (
                    "- TRAP (Guessing & Swapping Expensive Gear First): Replacing an NVR or camera before testing the patch cord, port, or power adapter wastes money.\n"
                    "- TRAP (Ignoring Rain/Night Patterns): Faults tied to rain often point to moisture ingress; faults at night often point to PoE/IR load."
                ),
                "diagram_or_visual_guide": (
                    "[Fault Reported] ---> [Test Short Patch & Port/PoE]\n"
                    "                 ---> [Check Cable Run & Outdoor Weather Seals]\n"
                    "                 ---> [Verify Recorder/Storage & Sustained Operation]"
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
                    "RESILIENCE, HARDENING & COMMERCIAL CLARITY:\n"
                    "- Power & Surge Protection: Pair NVRs, switches, and network gear with UPS backup and surge protection against power outages and voltage spikes.\n"
                    "- Credential Hardening: Replace factory default passwords on cameras, NVRs, and routers before handover, and set accurate date/time.\n"
                    "- Transparent Quoting & SLA: Itemize hardware, cabling/conduit/boxes, and labor separately, and offer scheduled inspection/maintenance plans."
                ),
                "step_by_step_field_guide": (
                    "PRE-HANDOVER CHECK:\n"
                    "- Confirm all cables are labelled, mounts are tight, and live/recorded/network checks pass.\n\n"
                    "HARDENING & HANDOVER STEPS:\n"
                    "1. Change default passwords, set accurate date/time, and verify UPS runtime on NVR/router.\n"
                    "2. Present itemized quote covering hardware, cabling/conduit/boxes, and installation labor.\n"
                    "3. Deliver labeled cable/camera map, login handover sheet, and maintenance plan option.\n\n"
                    "POST-HANDOVER CHECK:\n"
                    "- Walk the client through basic playback/app/intercom use and emergency contacts."
                ),
                "safety_and_traps": (
                    "- TRAP (Leaving Factory Default Passwords Active): Leaves security cameras and routers vulnerable to unauthorized access.\n"
                    "- TRAP (Under-Quoting Long Cable & Conduit Runs): Forgetting conduit, clips, boxes, and labor hours erodes project profit."
                ),
                "diagram_or_visual_guide": (
                    "[AC / Grid / Generator] ---> [Surge Protection + UPS]\n"
                    "                                    |\n"
                    "                                    v\n"
                    "            [NVR + PoE Switch + Router] ---> [Strong Passwords + Map + SLA]"
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

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=3,
            defaults={
                "title": "Step 7: Packet Loss, Latency & PoE Power-Budget Diagnostics Under Load",
                "estimated_minutes": 60,
                "is_free_preview": False,
                "learning_objectives": "- Diagnose intermittent streams, high latency, or packet loss using structured layer-by-layer checks.\n- Verify PoE power draw against switch wattage budgets so cameras and APs do not brown out under load.",
                "why_it_matters": "Devices may power up during light testing yet reboot or drop frames when IR night-vision LEDs or peak traffic load engage.",
                "core_explanation": "LOAD & POWER-BUDGET DIAGNOSTICS:\n- Compare total connected PoE load (including IR illumination, heaters, or intercoms) against the switch's available wattage budget.\n- Isolate faults systematically: physical link/cable -> PoE power/port -> IP/routing/bandwidth -> NVR/endpoint.\n\nFAULT ISOLATION TABLE:\nSymptom               | Likely Cause / Check\n----------------------+--------------------------------------------------\nCamera drops at night | IR LEDs push PoE draw over budget or voltage drop on long run\nChoppy/laggy stream   | High packet loss, duplex/link issue, or saturated link\nDevice offline        | Loose termination, dead port, or IP/gateway mismatch",
                "step_by_step_field_guide": "PRE-CHECK:\n- Note which cameras, intercoms, or APs drop, when they fail, and current switch PoE usage.\n\nDIAGNOSTIC STEPS:\n1. Check physical cable integrity, terminations, link lights, and port status.\n2. Add up PoE device draw under full load (such as night/IR mode) vs. switch budget.\n3. Test reachability/latency and packet loss between endpoints, recorder, and gateway.\n\nPOST-CHECK:\n- Rebalance loads or re-terminate/replace faulty runs and confirm sustained stability.",
                "safety_and_traps": "- TRAP (Testing Only in Daylight): Daytime PoE draw is lower without full IR illumination—always check night/peak load.\n- TRAP (Changing Multiple Settings at Once): Altering IPs, cables, and switch rules together hides the true root cause.",
                "diagram_or_visual_guide": "[Symptom Reported] ---> [Physical & PoE Budget Check] ---> [Latency / Packet Loss Test]\n                                                                       |\n                                              [Targeted Fix & Load Re-Verify]",
                "real_life_scenario": "Outdoor cameras stay online all afternoon but go offline after dark—checking PoE wattage under full IR load reveals the switch budget is exceeded.",
                "practice_activity": "Calculate PoE load for 6 cameras (9 W each at peak) plus 1 access point (13 W) and compare against a 90 W PoE budget.",
                "checkpoint_questions": "1. Why can a PoE switch pass daytime checks yet drop cameras at night?\n2. Why change one variable at a time during network or CCTV fault isolation?"
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=4,
            defaults={
                "title": "Step 8: Handover Checklists, Site As-Built Diagrams & Service-Level Agreements",
                "estimated_minutes": 50,
                "is_free_preview": False,
                "learning_objectives": "- Deliver a clear handover pack with as-built diagrams, credentials/settings record, and user walkthrough.\n- Structure maintenance plans and service-level expectations around response times and preventive visits.",
                "why_it_matters": "A clean handover and clear maintenance agreement prevent after-hours disputes and create predictable recurring service revenue.",
                "core_explanation": "HANDOVER & SERVICE AGREEMENTS:\n- Provide a clean as-built summary showing camera/intercom/AP placements, cable/port labels, and basic user instructions.\n- Define preventive maintenance intervals, response expectations, and covered vs. out-of-scope items clearly.\n\nHANDOVER & MAINTENANCE ESSENTIALS:\nDeliverable       | Purpose\n------------------+--------------------------------------------------\nAs-Built Summary  | Shows device locations, labels & basic system layout\nUser Walkthrough  | Trains client on live view, playback & intercom use\nMaintenance Plan  | Sets inspection cadence, response window & clear scope",
                "step_by_step_field_guide": "PRE-HANDOVER CHECK:\n- Confirm every camera angle, intercom call/unlock, network drop, and backup/UPS works as promised.\n\nHANDOVER STEPS:\n1. Walk the client through daily operation, playback/export basics, and safety/power notes.\n2. Share the as-built layout, port/device notes, and emergency/support contact details.\n3. Review maintenance schedule and response terms so both sides share clear expectations.\n\nPOST-HANDOVER CHECK:\n- Obtain sign-off and log follow-up check dates for ongoing support.",
                "safety_and_traps": "- TRAP (Leaving Default Passwords or No Records): Leaving default credentials or zero documentation creates security and support headaches.\n- TRAP (Vague Maintenance Promises): Unclear response times or scope cause friction when urgent faults arise.",
                "diagram_or_visual_guide": "[System Verified] ---> [As-Built Map & Client Demo] ---> [Signed Handover & Care Plan]",
                "real_life_scenario": "A business owner receives a simple one-page camera/IP map and a quarterly maintenance schedule—routine cleaning and checks catch loose connections before outages occur.",
                "practice_activity": "Write a concise handover checklist and preventive maintenance outline for a small office CCTV + LAN setup.",
                "checkpoint_questions": "1. What key items should be included when handing over a completed CCTV or network installation?\n2. Why put preventive maintenance intervals and response expectations in writing?"
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
            explanation="Changing default passwords protects cameras, NVRs, and network devices from unauthorized access.",
        )

        # =====================================================================
        # GLOSSARY TERMS (12 TERMS ACROSS TIER 1, TIER 2 & TIER 3)
        # =====================================================================
        glossary_items = [
            ("equipment", "IP Camera", "Internet Protocol Camera", "Network camera sending digital video streams over Ethernet/IP.", "Uses PoE or local power and connects to an NVR or switch.", True, 1),
            ("equipment", "Analog HD (TVI/CVI/AHD)", "HD over Coaxial Video Standards", "High-definition analog video formats transmitted over coaxial cable.", "Connects to a compatible DVR and helps upgrade older coax sites.", True, 2),
            ("equipment", "NVR / DVR", "Network / Digital Video Recorder", "Recorder storing video from IP cameras (NVR) or analog HD cameras (DVR).", "Pair with surveillance-rated HDDs and verify recording & playback.", True, 3),
            ("general", "PoE", "Power over Ethernet", "Delivers DC power and network data over a single twisted-pair cable.", "Check switch PoE wattage budget against total camera & IR load.", True, 4),
            ("equipment", "Cat6", "Category 6 Twisted-Pair Cable", "Structured Ethernet cable supporting high-speed data and PoE runs.", "Keep twists close to the RJ45 plug and test all 8 pins.", True, 5),
            ("tools", "T568B", "TIA/EIA-568-B Wiring Standard", "Common color pinout order for RJ45 Ethernet terminations.", "Maintains consistent pairing across patch cords and structured drops.", True, 6),
            ("equipment", "Intercom & Door Release", "Entry Audio/Video & Lock Control", "Communicates with visitors at an entry point and can release a door/gate lock.", "Verify call clarity, wiring continuity, and safe power/control routing.", False, 7),
            ("safety", "Drip Loop", "Low Cable Bend Before Entry", "Downward loop below a cable entry point so water drips off before reaching joints.", "Prevents rainwater from running along exterior cables into boxes or plugs.", False, 8),
            ("general", "DHCP / Static IP", "Dynamic vs. Fixed IP Addressing", "Automatic IP assignment vs. manually fixed IP address on a network.", "Helps locate cameras/NVRs reliably and avoid IP address conflicts.", False, 9),
            ("equipment", "Access Point (AP)", "Wireless LAN Access Point", "Creates or expands Wi-Fi coverage connected back to a wired switch/router.", "Place centrally and wired via Cat6 for stronger, cleaner coverage.", False, 10),
            ("safety", "SPD / UPS", "Surge Protective Device / Uninterruptible Power Supply", "Guards against voltage spikes and keeps critical gear powered during outages.", "Protects NVRs, switches, and routers from grid fluctuations and blackouts.", False, 11),
            ("business", "SLA / Maintenance Plan", "Service Level / Preventive Care Agreement", "Clear support scope and periodic inspection terms for client systems.", "Builds recurring revenue and keeps cameras, drives, and links healthy.", False, 12),
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
                "including diagrams, reference tables, glossary terms, and quizzes!"
            )
        )