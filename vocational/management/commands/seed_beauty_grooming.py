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
    help = "Seeds the complete 3-tier Barbing, Hairdressing, Makeup & Nail Art course, glossary, and quizzes."

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
            category.save()
        else:
            category = TradeCategory.objects.create(
                slug=target_slug,
                name=target_name,
                description=target_description,
            )

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
                    "Always brush/wash away hair or debris first, then immerse/wipe non-porous tools with "
                    "approved disinfectant for the required contact time, and use fresh/disposable items "
                    "where required. Consult the client on desired style/look, maintenance routine, and any "
                    "sensitivity or scalp/skin irritation."
                ),
                "step_by_step_field_guide": (
                    "1. Sanitize hands and prep a clean station with fresh towel/cape/neck strip.\n"
                    "2. Inspect client's hair, scalp, skin, or nails for irritation, cuts, or sensitivities.\n"
                    "3. Confirm style/shade/length expectations and perform a patch test before chemical/color/adhesive use.\n"
                    "4. Clean and disinfect tools after the service."
                ),
                "safety_and_traps": (
                    "TRAP: Spraying or wiping a dirty clipper blade or brush without removing hair/debris "
                    "and allowing proper disinfectant contact time."
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
                    "Keep wrists neutral, adjust chair/table height to your working elbow level rather than "
                    "hunching over clients, oil clipper blades lightly after sanitizing, and keep makeup "
                    "brushes/nail files organized and clean."
                ),
                "step_by_step_field_guide": (
                    "1. Arrange tools cleanly within reach without clutter.\n"
                    "2. Adjust seating/station height to protect your back, neck, and wrists.\n"
                    "3. Oil clipper blades and clean/store brushes/files properly after use."
                ),
                "safety_and_traps": (
                    "TRAP: Hunched posture all day leading to chronic neck/back pain, or leaving clipper "
                    "blades un-oiled so they snag hair and heat up."
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
                    "Work in structured sections from the bottom up, use flick/scoop motion with guards and "
                    "lever adjustments to soften harsh lines without pushing back natural hairlines, and "
                    "prioritize moisture, gentle detangling, and heat protection in hairstyling."
                ),
                "step_by_step_field_guide": (
                    "1. Comb hair in natural growth direction and set initial length/guideline.\n"
                    "2. Step through guards smoothly, blending lines with controlled wrist/lever motion.\n"
                    "3. Detangle gently from ends toward roots, condition/style cleanly, and check symmetry in mirror."
                ),
                "safety_and_traps": (
                    "TRAP: Pushing natural hairlines too far back with sharp trimmers or over-filing/over-heating fragile hair."
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
                    "Match base shades to undertone and test along the jawline/neck in good light, blend "
                    "edges seamlessly, and for nails: shape evenly, push/clean cuticles gently without "
                    "damaging live skin, apply thin even coats, and seal free edges."
                ),
                "step_by_step_field_guide": (
                    "1. Prep clean skin/nails and confirm desired look/finish with client.\n"
                    "2. Apply thin, blendable layers rather than heavy buildup at once.\n"
                    "3. Seal nail free edges and inspect final look in natural/balanced lighting."
                ),
                "safety_and_traps": (
                    "TRAP: Applying thick layers of polish or foundation all at once, causing smudging, "
                    "creasing, or uneven texture."
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
                    "price services/packages/bridal or event bookings profitably, build a portfolio, "
                    "manage appointments, and earn QR-verifiable certification."
                ),
                "tier": "tier_3",
                "is_free_tier": False,
                "level": "Advanced",
                "duration_hours": 12,
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
                    "Factor in product/consumable cost, chair/kit overhead, travel time (for mobile/events), "
                    "and your skilled time. If a client asks for a minor adjustment right after a service, "
                    "listen calmly and address reasonable fixes politely while setting clear expectations."
                ),
                "step_by_step_field_guide": (
                    "1. Build a clear price list covering base services, add-ons, and event/mobile rates.\n"
                    "2. Confirm scope, timing, and booking terms before starting.\n"
                    "3. Follow up politely on care/maintenance and ask satisfied clients for referrals."
                ),
                "safety_and_traps": (
                    "TRAP: Accepting last-minute underpriced event/group bookings without time buffers or clear scope."
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
        # GLOSSARY TERMS (AVAILABLE FROM TIER 1 & ACROSS ALL THREE TIERS)
        # =====================================================================
        glossary_items = [
            ("safety", "Disinfection", "Antimicrobial Surface & Tool Treatment", "Reduces harmful microorganisms on cleaned non-porous tools and surfaces.", "Clean debris first, then apply disinfectant for full contact time.", True, 1),
            ("safety", "Patch Test", "Small-Area Skin Sensitivity Check", "Tests a small area ahead of full application to check for irritation/allergy.", "Helps identify sensitivities before color, chemical, or adhesive services.", True, 2),
            ("equipment", "Guard / Lever", "Clipper Attachment Comb & Blade Taper Lever", "Controls cutting length and helps blend transitions smoothly.", "Adjust gradually and check symmetry from multiple angles.", True, 3),
            ("general", "Porosity", "Ability of Hair/Nail to Absorb & Hold Moisture", "Influences how products penetrate, process, and retain moisture.", "Guides product selection and gentle moisture/strengthening care.", True, 4),
            ("business", "Service Scope", "Agreed Deliverables, Add-Ons & Time Window", "Clear agreement on what a session or event booking includes.", "Prevents misunderstandings on pricing, duration, and extras.", False, 5),
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
                "including lessons, glossary terms, and quizzes!"
            )
        )