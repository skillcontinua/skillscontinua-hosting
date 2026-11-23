# File path: C:\hosting\skillscontinua_hosting\vocational\management\commands\seed_beauty_grooming.py
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
        "Seeds the complete 3-tier Barbing, Hairdressing, Makeup & Nail Art course, "
        "diagrams, reference tables, glossary, and quizzes."
    )

    def handle(self, *args, **options):
        target_slug = "barbing-hairdressing-makeup-nail-art"
        target_name = "Barbing, Hairdressing, Makeup & Nail Art"
        target_description = (
            "Practical salon & studio training covering hygiene & sterilization, client skin/hair/nail "
            "consultation, clippers & hair care, styling/braiding/treatment, makeup artistry, "
            "nail care & extensions, and salon business operations."
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
        # TIER 1 (FREE): HYGIENE, CLIENT CONSULTATION & TOOL BASICS
        # =====================================================================
        tier1_course, _ = TradeCourse.objects.update_or_create(
            slug="beauty-grooming-tier-1-foundation",
            defaults={
                "category": category,
                "title": "Barbing, Hairdressing, Makeup & Nail Art — Tier 1: Hygiene & Consultation",
                "description": (
                    "FREE TIER: Master salon hygiene & tool sanitation, skin/scalp/nail safety checks, "
                    "client consultation, tool care, and essential beauty & grooming terminology."
                ),
                "tier": "tier_1",
                "is_free_tier": True,
                "level": "Foundation",
                "duration_hours": 6,
                "credential_awarded": "Tier 1 Salon Hygiene & Client Consultation Readiness Record",
                "required_tools": (
                    "Disinfectant / Barbicide-Type Sanitizing Solution, Clean Towels & Neck Strips, "
                    "Disposable Gloves & Applicators, Clippers / Combs / Brushes / Nail Files, "
                    "Mirror & Consultation Checklist"
                ),
                "safety_guidelines": (
                    "1. SANITATION FIRST: Clean visible debris and disinfect clippers, blades, combs, brushes, "
                    "and nail tools between every single client—never reuse contaminated blades or sponges.\n"
                    "2. SKIN & ALLERGY SCREENING: Check for rashes, open cuts, infections, or product allergies "
                    "before applying chemicals, heat, or cosmetics.\n"
                    "3. ELECTRICAL & HEAT CARE: Keep cords away from wet stations/water and avoid scorching skin or hair."
                ),
                "field_tips_summary": (
                    "Clients judge a salon or mobile artist within 30 seconds by cleanliness, fresh towels/blades, "
                    "and listening closely to what they actually want—good hygiene wins repeat customers."
                ),
                "course_glossary_overview": (
                    "Covers Sanitization vs. Disinfection vs. Sterilization, Patch Test, Guard/Fade, "
                    "Porosity & Elasticity, Primer / Base / Top Coat, and Cross-Contamination."
                ),
                "is_featured": True,
            },
        )

        mod1, _ = TradeModule.objects.update_or_create(
            trade_course=tier1_course,
            order=1,
            defaults={
                "title": "Module 1: Salon Hygiene, Client Consultation & Core Beauty Foundations",
                "tier": "tier_1",
                "summary": "Build spotless hygiene habits, conduct clear consultations, and master key terms.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=1,
            defaults={
                "title": "Step 1: Salon Hygiene, Tool Disinfection & Client Skin/Hair Consultation",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Clean and disinfect tools/surfaces between clients to prevent infection.\n"
                    "- Run a clear client consultation, spot contraindications, and run patch tests when needed."
                ),
                "why_it_matters": (
                    "Poor hygiene spreads fungal, bacterial, and viral skin/nail/scalp issues and destroys "
                    "a beauty business's reputation fast."
                ),
                "core_explanation": (
                    "HYGIENE & CONSULTATION STANDARDS:\n"
                    "- Clean Before Disinfecting: Always brush or wash away hair, oil, or debris first, then apply approved disinfectant for the full contact time and use fresh/disposable items where required.\n"
                    "- Client Screening & Patch Testing: Check scalp, skin, and nails for irritation, cuts, or infection signs, confirm expectations, and patch-test before chemical/color/adhesive application.\n\n"
                    "HYGIENE & SCREENING REFERENCE:\n"
                    "Check Area       | Key Rule / Standard\n"
                    "-----------------+--------------------------------------------------------\n"
                    "Non-Porous Tools | Remove debris first -> disinfect for full contact time\n"
                    "Skin / Scalp     | Inspect for cuts/rash/infection; patch-test if needed\n"
                    "Station / Chair  | Fresh neck strip/towel & sanitized surface per client"
                ),
                "step_by_step_field_guide": (
                    "PRE-SESSION CHECK:\n"
                    "- Sanitize hands, prep a clean station, and place a fresh towel/cape/neck strip.\n\n"
                    "CONSULTATION & HYGIENE STEPS:\n"
                    "1. Sanitize hands and prep a clean station with fresh towel/cape/neck strip.\n"
                    "2. Inspect client's hair, scalp, skin, or nails for irritation, cuts, or sensitivities.\n"
                    "3. Confirm style/shade/length expectations and perform a patch test before chemical/color/adhesive use.\n"
                    "4. Clean and disinfect tools after the service.\n\n"
                    "POST-SESSION CHECK:\n"
                    "- Dispose of single-use items safely and reset the station for the next client."
                ),
                "safety_and_traps": (
                    "- TRAP (Disinfecting Over Dirt/Hair): Wiping or spraying a dirty blade or brush without removing debris reduces disinfectant effectiveness.\n"
                    "- TRAP (Rushing Past Red Flags): Ignoring inflamed scalp/skin or skipping patch tests can trigger severe reactions."
                ),
                "diagram_or_visual_guide": (
                    "[Client Arrives] ---> [Consultation + Scalp/Skin/Nail Check]\n"
                    "                                     |\n"
                    "       +-----------------------------+ (Service Performed)\n"
                    "       v\n"
                    "[Remove Debris] ---> [Disinfect / Full Contact Time] ---> [Clean Station Ready]"
                ),
                "real_life_scenario": (
                    "A client arrives with an inflamed, flaky patch on their scalp—pausing chemical "
                    "relaxer/color and advising care protects the client and prevents a severe reaction."
                ),
                "practice_activity": (
                    "Write a 5-point client consultation & hygiene checklist for barbing, hair, makeup, or nails."
                ),
                "checkpoint_questions": (
                    "1. Why must debris be removed before disinfecting a tool?\n"
                    "2. Why run a patch test before applying hair color, chemicals, or adhesives?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod1,
            order=2,
            defaults={
                "title": "Step 2: Core Tools, Ergonomics & Beauty/Grooming Terminology",
                "estimated_minutes": 45,
                "is_free_preview": True,
                "learning_objectives": (
                    "- Handle clippers, combs, brushes, makeup applicators, and nail tools with good posture.\n"
                    "- Understand core terms across barbing, hairdressing, makeup, and nail art."
                ),
                "why_it_matters": (
                    "Proper tool grip and ergonomic posture prevent wrist/back strain over long busy days "
                    "and improve precision."
                ),
                "core_explanation": (
                    "ERGONOMICS & TOOL CARE:\n"
                    "- Keep wrists neutral and adjust chair/table height to your working elbow level rather than hunching over clients.\n"
                    "- Brush out hair/dust, oil clipper blades lightly after sanitizing, and store combs, brushes, and nail tools cleanly."
                ),
                "step_by_step_field_guide": (
                    "PRE-WORK CHECK:\n"
                    "- Check blade alignment/cord condition and keep essential tools organized within reach.\n\n"
                    "ERGONOMIC & TOOL STEPS:\n"
                    "1. Arrange tools cleanly within reach without clutter.\n"
                    "2. Adjust seating/station height to protect your back, neck, and wrists.\n"
                    "3. Oil clipper blades and clean/store brushes/files properly after use.\n\n"
                    "POST-WORK CHECK:\n"
                    "- Verify cords are untangled/safe and tools are stored dry and clean."
                ),
                "safety_and_traps": (
                    "- TRAP (Chronic Slouching/Hunching): Bending low all day causes neck, shoulder, and lower-back strain.\n"
                    "- TRAP (Dry/Un-Oiled Clipper Blades): Dry blades snag hair, generate excess heat, and wear faster."
                ),
                "diagram_or_visual_guide": (
                    "[Station & Chair Height] ---> [Neutral Wrist + Elbow-Level Reach]\n"
                    "                                       |\n"
                    "                                       v\n"
                    "                     [Clean/Oil Blades & Brushes After Use]"
                ),
                "real_life_scenario": (
                    "Clippers pull hair and run hot during a busy Saturday—cleaning hair buildup, checking "
                    "blade alignment, and applying clipper oil restores smooth cutting."
                ),
                "practice_activity": (
                    "Practice ergonomic stance and tool grip for 10 minutes and list 6 key terms from the glossary."
                ),
                "checkpoint_questions": (
                    "1. How does station/chair height affect long-term artist health?\n"
                    "2. Why oil clipper blades after cleaning?"
                ),
            },
        )

        tier1_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 1 Salon Hygiene, Consultation & Foundations Quiz",
            trade_course=tier1_course,
            trade_module=mod1,
            defaults={
                "tier": "tier_1",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 20,
                "instructions": "Verify salon hygiene, client consultation, ergonomics, and core terms.",
            },
        )
        tier1_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier1_quiz,
            order=1,
            is_scenario_question=True,
            text="A client asks for a hair dye or lash/brow service and mentions having had allergic reactions to beauty products in the past. What should you do?",
            option_a="Conduct a proper consultation and patch test first, and avoid proceeding if signs of sensitivity/irritation appear",
            option_b="Apply full product immediately without checking ingredients",
            option_c="Tell the client allergies never happen twice",
            option_d="Skip hygiene steps to finish faster",
            correct_answer="A",
            explanation="Client safety comes first; screening and patch testing help prevent adverse skin/allergic reactions.",
        )
        Question.objects.create(
            quiz=tier1_quiz,
            order=2,
            text="Why should tools be cleaned of visible hair, product, or debris before applying disinfectant?",
            option_a="Debris can shield microbes and reduce disinfectant effectiveness",
            option_b="Disinfectant only works on dry hair clumps",
            option_c="It changes the color of the tool handle",
            option_d="Cleaning is optional if the tool looks shiny",
            correct_answer="A",
            explanation="Effective sanitation requires removing physical soil first so the disinfectant contacts the surface directly.",
        )

        # =====================================================================
        # TIER 2 (AFFORDABLE): BARBING, HAIR, MAKEUP & NAIL PRACTICAL TECHNIQUES
        # =====================================================================
        tier2_course, _ = TradeCourse.objects.update_or_create(
            slug="beauty-grooming-tier-2-proficiency",
            defaults={
                "category": category,
                "title": "Barbing, Hairdressing, Makeup & Nail Art — Tier 2: Hands-On Craft Mastery",
                "description": (
                    "PRACTICAL PROFICIENCY TIER: Execute clean clipper/scissor cuts and fades, natural/treated "
                    "hair care & styling, undertone-matched makeup application, and neat prep/manicure/nail "
                    "art finishes."
                ),
                "tier": "tier_2",
                "is_free_tier": False,
                "level": "Intermediate",
                "duration_hours": 14,
                "credential_awarded": "Tier 2 Practical Grooming, Hair, Makeup & Nail Certificate",
                "required_tools": (
                    "All Tier 1 tools plus Clipper Guards & Trimmer, Hair Styling/Sectioning Clips, "
                    "Foundation/Concealer/Blending Brushes, Nail Prep/Cuticle/Polish & Tip Kit"
                ),
                "safety_guidelines": (
                    "1. EVEN TENSION & GENTLE HANDLING: Avoid harsh tugging on hair roots, excessive filing on "
                    "natural nail plates, or heavy pressure around delicate eye areas.\n"
                    "2. SHADE & MOISTURE BALANCE: Match makeup shades in natural/balanced light and keep hair/skin "
                    "hydrated rather than overly dry/brittle.\n"
                    "3. CLEAN EDGES & FINISHES: Check symmetry from front, sides, and back before calling a look complete."
                ),
                "field_tips_summary": (
                    "Prep is 70% of the result—smooth skin prep makes makeup blend effortlessly, clean nail "
                    "prep makes polish/extensions last, and consistent guidelines make clean fades."
                ),
                "course_glossary_overview": (
                    "Covers Fade / Lever Adjustment, Hair Porosity & Moisture-Protein Balance, "
                    "Skin Undertone (Warm/Cool/Neutral), Cuticle Care, Base/Top Coat, and Symmetry Check."
                ),
                "is_featured": True,
            },
        )

        mod2, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=1,
            defaults={
                "title": "Module 2: Barbing & Hairdressing Craft (Cuts, Fades, Care & Styling)",
                "tier": "tier_2",
                "summary": "Build clean clipper/fade control, healthy hair care, and neat styling finishes.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod2,
            order=1,
            defaults={
                "title": "Step 3: Clipper Control, Blending/Fades & Healthy Hair Care/Styling",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Establish clean guidelines, blend guard transitions smoothly, and line up edges carefully.\n"
                    "- Handle natural and treated hair gently while cleansing, conditioning, and styling."
                ),
                "why_it_matters": (
                    "Crisp blends, natural hairlines, and healthy hair care turn first-time clients into loyal regulars."
                ),
                "core_explanation": (
                    "CLIPPER BLENDING & HAIR CARE:\n"
                    "- Work in structured sections from the bottom up, using controlled flick/scoop motion with guards and lever adjustments to soften harsh lines while preserving natural hairlines.\n"
                    "- Detangle gently from ends toward roots with moisture/slip, and protect hair against excessive heat or tension.\n\n"
                    "CRAFT & CARE BENCHMARK:\n"
                    "Area              | Key Standard\n"
                    "------------------+--------------------------------------------------\n"
                    "Fades & Blends    | Clean guideline + gradual guard/lever transitions\n"
                    "Hairline / Edges  | Crisp yet natural—avoid pushing hairlines back\n"
                    "Detangling/Styling| Start at ends, add moisture/slip, check symmetry"
                ),
                "step_by_step_field_guide": (
                    "PRE-SERVICE CHECK:\n"
                    "- Confirm guard/length/style expectations and inspect hair/scalp condition.\n\n"
                    "CRAFT STEPS:\n"
                    "1. Comb hair in natural growth direction and set initial length/guideline.\n"
                    "2. Step through guards smoothly, blending lines with controlled wrist/lever motion.\n"
                    "3. Detangle gently from ends toward roots, condition/style cleanly, and check symmetry in mirror.\n\n"
                    "POST-SERVICE CHECK:\n"
                    "- Inspect front, left/right profiles, and back in balanced light before finishing."
                ),
                "safety_and_traps": (
                    "- TRAP (Pushing Back Hairlines): Over-lining with sharp trimmers pushes natural hairlines back and looks harsh as it grows.\n"
                    "- TRAP (Rough Root-to-Tip Tugging): Pulling knots from the root causes breakage and client discomfort."
                ),
                "diagram_or_visual_guide": (
                    "[Natural Growth / Section] ---> [Set Guideline] ---> [Guard/Lever Blend]\n"
                    "                                                       |\n"
                    "   [Front / Sides / Back Symmetry Check] <---------------+ (Detangle Ends-Up / Style)"
                ),
                "real_life_scenario": (
                    "A client asks for a clean, natural look that grows out neatly over two weeks—keeping a "
                    "natural hairline and smooth gradient avoids harsh lines as hair grows."
                ),
                "practice_activity": (
                    "Practice blending a smooth transition across two guard sizes and check symmetry from "
                    "front, profile, and back angles."
                ),
                "checkpoint_questions": (
                    "1. Why is keeping a natural hairline important in barbing?\n"
                    "2. When detangling hair, where should you start—at the roots or at the ends?"
                ),
            },
        )

        mod3, _ = TradeModule.objects.update_or_create(
            trade_course=tier2_course,
            order=2,
            defaults={
                "title": "Module 3: Makeup Artistry & Nail Care / Nail Art Execution",
                "tier": "tier_2",
                "summary": "Deliver balanced makeup looks and durable, tidy manicures and nail finishes.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod3,
            order=1,
            defaults={
                "title": "Step 4: Skin Prep, Shade Matching, Makeup Blending & Nail Care / Finishes",
                "estimated_minutes": 60,
                "learning_objectives": (
                    "- Prep skin, match undertone/complexion naturally, and blend makeup without harsh lines.\n"
                    "- Shape, prep, and finish nails cleanly with smooth edges and lasting polish/coatings."
                ),
                "why_it_matters": (
                    "Ashy foundation or lifted/uneven nails are easy to spot—mastering prep and blending "
                    "makes your work look polished in person and in photos."
                ),
                "core_explanation": (
                    "MAKEUP & NAIL FINISH STANDARDS:\n"
                    "- Match base shades to undertone and test along the jawline/neck in balanced light, blending edges seamlessly in thin layers.\n"
                    "- For nails: shape evenly, prep gently without over-filing live nail plates, apply thin even coats, and seal the free edge.\n\n"
                    "MAKEUP & NAIL QUALITY CHECK:\n"
                    "Craft        | Primary Detail to Nail\n"
                    "-------------+-----------------------------------------------------\n"
                    "Makeup Base  | Undertone match + seamless jawline/neck blend\n"
                    "Nail Prep    | Gentle shaping & cuticle care without thinning plate\n"
                    "Nail Finish  | Thin even coats + sealed free edge for longevity"
                ),
                "step_by_step_field_guide": (
                    "PRE-SERVICE CHECK:\n"
                    "- Confirm skin/nail condition and check undertone/finish preferences in good light.\n\n"
                    "APPLICATION STEPS:\n"
                    "1. Prep clean skin/nails and confirm desired look/finish with client.\n"
                    "2. Apply thin, blendable layers rather than heavy buildup at once.\n"
                    "3. Seal nail free edges and inspect final look in natural/balanced lighting.\n\n"
                    "POST-SERVICE CHECK:\n"
                    "- Check for harsh edges, uneven product pooling, or unsealed tips before client leaves."
                ),
                "safety_and_traps": (
                    "- TRAP (Thick Single-Coat Buildup): Applying thick layers of polish or foundation all at once causes smudging, creasing, or lifting.\n"
                    "- TRAP (Over-Filing Natural Nails): Aggressive filing weakens the nail plate and causes pain/lifting."
                ),
                "diagram_or_visual_guide": (
                    "[Clean Skin / Prepped Nail] ---> [Thin Buildable Layers] ---> [Seal Edges / Blend]\n"
                    "                                                                   |\n"
                    "                                                                   v\n"
                    "                                             [Natural / Balanced Light Inspection]"
                ),
                "real_life_scenario": (
                    "A client's foundation looks slightly too light in daylight—checking undertone and "
                    "blending down toward the neck/jawline in balanced light prevents mismatch."
                ),
                "practice_activity": (
                    "Complete a full makeup look or manicure/nail-art set and inspect edges, blending, "
                    "and finish under bright light."
                ),
                "checkpoint_questions": (
                    "1. Why apply thin, buildable layers instead of one thick coat in makeup or nail polish?\n"
                    "2. What does sealing the free edge of a nail help prevent?"
                ),
            },
        )

        tier2_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 2 Practical Beauty, Grooming & Nail Craft Quiz",
            trade_course=tier2_course,
            trade_module=mod3,
            defaults={
                "tier": "tier_2",
                "quiz_type": "module_test",
                "passing_score_percentage": 75,
                "time_limit_minutes": 25,
                "instructions": "Test blending, hair care, makeup shade/layering, and nail finish discipline.",
            },
        )
        tier2_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier2_quiz,
            order=1,
            is_scenario_question=True,
            text="When detangling hair that has knots or texture, what is the gentlest and most effective practice?",
            option_a="Start gently at the ends with slip/conditioning and work upward toward the roots",
            option_b="Rip a fine comb straight from the root to the tip forcefully",
            option_c="Pull knots dry with zero moisture or care",
            option_d="Skip detangling completely",
            correct_answer="A",
            explanation="Working from the ends upward reduces pulling, breakage, and client discomfort.",
        )
        Question.objects.create(
            quiz=tier2_quiz,
            order=2,
            text="Why do beauty and nail artists apply thin, even layers rather than thick coats all at once?",
            option_a="Thin layers blend/cure more evenly and reduce clumping, smudging, or lifting",
            option_b="Thick coats dry instantly with zero flaws",
            option_c="Thin layers save product only by spilling it",
            option_d="Layering is never needed",
            correct_answer="A",
            explanation="Controlled, thin layers give smoother finishes and better durability.",
        )

        # =====================================================================
        # TIER 3 (PROFESSIONAL): CLIENT RETENTION, PRICING, BRIDAL/EVENTS & BUSINESS
        # =====================================================================
        tier3_course, _ = TradeCourse.objects.update_or_create(
            slug="beauty-grooming-tier-3-professional",
            defaults={
                "category": category,
                "title": "Barbing, Hairdressing, Makeup & Nail Art — Tier 3: Client Care, Pricing & Business",
                "description": (
                    "PROFESSIONAL MASTERY TIER: Handle challenging client requests & touch-ups calmly, "
                    "price services/packages/bridal or event bookings profitably, manage event/mobile "
                    "workflows, build a portfolio, and earn QR-verifiable certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 14,
                "credential_awarded": "Tier 3 Master Beauty & Grooming Practitioner QR Certificate",
                "required_tools": (
                    "All Tier 1 & Tier 2 tools plus Portable / Mobile Kit Case (if doing home/event service), "
                    "Appointment & Service Pricing Log, Portfolio Camera/Lighting Setup"
                ),
                "safety_guidelines": (
                    "1. PUNCTUALITY & TIME BUFFERS: Buffer event/bridal/group bookings so rushed work never causes mistakes.\n"
                    "2. CLEAR SERVICE BOUNDARIES: Confirm exact scope, add-ons, and deposit/cancellation terms upfront.\n"
                    "3. RESPECT & PRIVACY: Keep client consultations discreet and ask permission before sharing photos."
                ),
                "field_tips_summary": (
                    "Price your time, product cost, travel, and skill fairly—undercharging burns you out "
                    "and forces you to cut corners on hygiene and quality."
                ),
                "course_glossary_overview": (
                    "Covers Service Menu / Add-Ons, Bridal/Event Trial & Deposit, Portfolio Lighting, "
                    "Client Retention, and Mobile vs. Studio Overhead."
                ),
                "is_featured": True,
            },
        )

        mod4, _ = TradeModule.objects.update_or_create(
            trade_course=tier3_course,
            order=1,
            defaults={
                "title": "Module 4: Client Experience, Service Pricing & Salon/Mobile Business Growth",
                "tier": "tier_3",
                "summary": "Turn practical skills into a reliable, respected salon or mobile beauty business.",
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=1,
            defaults={
                "title": "Step 5: Pricing Services & Packages, Handling Feedback & Building Repeat Clients",
                "estimated_minutes": 50,
                "learning_objectives": (
                    "- Price standard services, add-ons, and event/group bookings profitably.\n"
                    "- Handle client feedback professionally and build repeat bookings and referrals."
                ),
                "why_it_matters": (
                    "Great hands get you started, but clear pricing, reliability, and calm client care "
                    "keep chairs/bookings full year-round."
                ),
                "core_explanation": (
                    "PROFITABLE PRICING & CLIENT RETENTION:\n"
                    "- Factor in product/consumable cost, chair/kit overhead, travel time (for mobile/events), and your skilled time.\n"
                    "- If a client asks for a minor adjustment right after a service, listen calmly and address reasonable fixes politely while setting clear expectations.\n\n"
                    "PRICING & RETENTION ELEMENTS:\n"
                    "Element           | Purpose\n"
                    "------------------+---------------------------------------------------\n"
                    "Base + Add-On Menu| Clarifies what is included vs. optional extras\n"
                    "Mobile / Event Fee| Covers travel time, transport, and setup buffers\n"
                    "Follow-Up & Care  | Helps clients maintain results and refer others"
                ),
                "step_by_step_field_guide": (
                    "PRE-BOOKING CHECK:\n"
                    "- Confirm service scope, add-ons, estimated time, and price before starting.\n\n"
                    "PRICING & CLIENT CARE STEPS:\n"
                    "1. Build a clear price list covering base services, add-ons, and event/mobile rates.\n"
                    "2. Confirm scope, timing, and booking terms before starting.\n"
                    "3. Follow up politely on care/maintenance and ask satisfied clients for referrals.\n\n"
                    "POST-SESSION CHECK:\n"
                    "- Note client preferences for future visits and keep sanitation/kit restocked."
                ),
                "safety_and_traps": (
                    "- TRAP (Underpriced Rush Bookings): Accepting last-minute underpriced event/group bookings without time buffers or clear scope leads to stress and errors.\n"
                    "- TRAP (Defensive Reactions): Arguing over minor adjustments damages trust faster than a small fix."
                ),
                "diagram_or_visual_guide": (
                    "[Clear Scope & Quote] ---> [Timely + Hygienic Delivery] ---> [Follow-Up & Referrals]\n"
                    "                                                               |\n"
                    "                                                               v\n"
                    "                                                [Repeat Bookings & Steady Income]"
                ),
                "real_life_scenario": (
                    "A client wants a slight adjustment to blend/length right at the end of a session—staying "
                    "calm, checking what is possible safely, and finishing cleanly turns tension into loyalty."
                ),
                "practice_activity": (
                    "Create a service price & add-on sheet for your chosen specialty (barbing, hair, "
                    "makeup, or nails) including a mobile/event option."
                ),
                "checkpoint_questions": (
                    "1. What costs should be considered when pricing salon or mobile services?\n"
                    "2. Why confirm service scope and timing before starting?"
                ),
            },
        )

        TradeLesson.objects.update_or_create(
            module=mod4,
            order=2,
            defaults={
                "title": "Step 6: Event/Bridal Scheduling, Mobile Kit Readiness & Quality Standards",
                "estimated_minutes": 50,
                "learning_objectives": (
                    "- Plan event, bridal, or multi-client schedules with realistic time buffers.\n"
                    "- Maintain portable hygiene, lighting, and documentation standards for studio, mobile, or partner programs."
                ),
                "why_it_matters": (
                    "Running late on an event day or showing up to a home/community session with a messy, "
                    "unhygienic kit costs major opportunities with clients and institutional partners."
                ),
                "core_explanation": (
                    "EVENT WORKFLOW & PORTABLE STANDARDS:\n"
                    "- Build realistic per-person time estimates plus a buffer for setup, touch-ups, and unexpected delays.\n"
                    "- Keep a dedicated portable kit with fresh disposables, sealed sanitizers, good lighting, and clear client consent before taking portfolio photos."
                ),
                "step_by_step_field_guide": (
                    "PRE-EVENT CHECK:\n"
                    "- Pack and verify all tools, disposables, backups, and schedule/call times the day before.\n\n"
                    "EVENT & QUALITY STEPS:\n"
                    "1. Map out person-by-person timings with a buffer window and confirm arrival details.\n"
                    "2. Set up a clean, well-lit station and protect hygiene even on mobile/event locations.\n"
                    "3. Request client permission before capturing portfolio photos and log lessons learned.\n\n"
                    "POST-EVENT CHECK:\n"
                    "- Clean/sanitize all tools and replenish used supplies before the next booking."
                ),
                "safety_and_traps": (
                    "- TRAP (Zero Schedule Buffer): Booking back-to-back clients with zero cushion causes rushing and mistakes.\n"
                    "- TRAP (Posting Client Photos Without Permission): Always ask consent before sharing client images publicly."
                ),
                "diagram_or_visual_guide": (
                    "[Day-Before Kit & Schedule Check] ---> [Buffered On-Site Execution]\n"
                    "                                                      |\n"
                    "                                                      v\n"
                    "                            [Consented Portfolio + Full Kit Reset]"
                ),
                "real_life_scenario": (
                    "A bridal/event booking has four people getting ready before a tight ceremony time—"
                    "assigning clear time slots with a buffer keeps everyone calm and on schedule."
                ),
                "practice_activity": (
                    "Build a 4-person event/appointment timeline with time buffers and a pre-departure kit checklist."
                ),
                "checkpoint_questions": (
                    "1. Why include a buffer when scheduling event or group beauty bookings?\n"
                    "2. What should you do before taking or sharing photos of a client's look?"
                ),
            },
        )

        tier3_quiz, _ = Quiz.objects.update_or_create(
            title="Tier 3 Master Client Care, Pricing & Business Capstone Exam",
            trade_course=tier3_course,
            trade_module=mod4,
            defaults={
                "tier": "tier_3",
                "quiz_type": "final_exam",
                "passing_score_percentage": 80,
                "time_limit_minutes": 30,
                "instructions": "Capstone exam for Tier 3 Master Beauty & Grooming Practitioner QR Certificate.",
            },
        )
        tier3_quiz.questions.all().delete()
        Question.objects.create(
            quiz=tier3_quiz,
            order=1,
            is_scenario_question=True,
            text="A client expresses mild dissatisfaction with a detail at the end of a session. What is the most professional response?",
            option_a="Listen calmly without defensiveness, assess what can be adjusted safely, and explain options clearly",
            option_b="Argue loudly in front of other clients",
            option_c="Ignore the client and walk away",
            option_d="Skip sanitation on the next client to save time",
            correct_answer="A",
            explanation="Calm, respectful problem-solving protects your reputation and often turns a concern into repeat business.",
        )
        Question.objects.create(
            quiz=tier3_quiz,
            order=2,
            is_scenario_question=True,
            text="Why is pricing consumable supplies, time, and mobile/event travel separately or transparently important?",
            option_a="It prevents hidden losses and ensures every booking remains sustainable and high-quality",
            option_b="Because consumables cost zero",
            option_c="So clients never know what they are paying for",
            option_d="It is only used when closing a business",
            correct_answer="A",
            explanation="Accounted costs keep your business profitable so you can maintain high standards.",
        )

        # =====================================================================
        # GLOSSARY TERMS (12 TERMS ACROSS TIER 1, TIER 2 & TIER 3)
        # =====================================================================
        glossary_items = [
            ("safety", "Disinfection", "Antimicrobial Surface & Tool Treatment", "Reduces harmful microorganisms on cleaned non-porous tools and surfaces.", "Clean debris first, then apply disinfectant for full contact time.", True, 1),
            ("safety", "Patch Test", "Small-Area Skin Sensitivity Check", "Tests a small area ahead of full application to check for irritation/allergy.", "Helps identify sensitivities before color, chemical, or adhesive services.", True, 2),
            ("equipment", "Guard / Lever", "Clipper Attachment Comb & Blade Taper Lever", "Controls cutting length and helps blend transitions smoothly.", "Adjust gradually and check symmetry from multiple angles.", True, 3),
            ("general", "Porosity", "Ability of Hair/Nail to Absorb & Hold Moisture", "Influences how products penetrate, process, and retain moisture.", "Guides product selection and gentle moisture/strengthening care.", True, 4),
            ("safety", "Cross-Contamination", "Unintended Transfer of Microbes or Residue", "Happens when shared tools, towels, or hands carry contaminants between clients.", "Sanitize/disinfect tools and use clean barriers between every client.", True, 5),
            ("general", "Skin Undertone", "Warm, Cool, or Neutral Base Tone Under Skin", "Guides foundation/concealer matching so shades look natural rather than ashy/orange.", "Test along jawline/neck in balanced light before finalizing shade.", False, 6),
            ("equipment", "Free Edge", "Unattached Tip of the Nail Plate", "The front edge of the nail extending past the finger bed.", "Shape evenly and seal with base/top/finish coat to prevent lifting.", False, 7),
            ("tools", "Clipper Oil", "Lubricant for Clipper Blades", "Reduces friction, heat, and wear between moving cutter and stationary blades.", "Clean hair/debris first and apply a few drops regularly.", False, 8),
            ("business", "Service Scope", "Agreed Deliverables, Add-Ons & Time Window", "Clear agreement on what a session or event booking includes.", "Prevents misunderstandings on pricing, duration, and extras.", False, 9),
            ("business", "Time Buffer", "Extra Schedule Cushion Between Bookings", "Planned slack time to absorb setup, consultation, or minor delays.", "Keeps event/salon appointments running smoothly without rushed mistakes.", False, 10),
            ("business", "Mobile Kit", "Portable Case for Home or Event Services", "Organized travel kit holding sanitized tools, disposables, and essentials.", "Protects hygiene and speed when working outside a fixed salon chair.", False, 11),
            ("business", "Client Retention", "Repeat Visits & Word-of-Mouth Referrals", "Earned through consistent quality, hygiene, fair pricing, and polite care.", "Turns one-time clients into steady income over time.", False, 12),
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
                "Seeded Barbing, Hairdressing, Makeup & Nail Art across Tier 1, Tier 2, and Tier 3, "
                "including diagrams, reference tables, glossary terms, and quizzes!"
            )
        )