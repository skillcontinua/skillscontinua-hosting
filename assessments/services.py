# File path: C:\hosting\skillscontinua_hosting\assessments\services.py
import hashlib
import uuid
from urllib.parse import quote
from django.utils import timezone
from .models import Quiz, Question, UserProgress, Certificate, CompetencyTranscript


def classify_grade(score_percentage: float) -> str:
    if score_percentage >= 90.0:
        return "Distinction"
    if score_percentage >= 80.0:
        return "Merit"
    if score_percentage >= 75.0:
        return "Pass"
    return "Needs Retake"


def generate_verification_code(prefix: str, user_id: int, course_id: int, tier: str) -> str:
    raw = f"{prefix}:{user_id}:{course_id}:{tier}:{uuid.uuid4()}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12].upper()
    return f"SC-{prefix}-{digest}"


def build_qr_verification_url(verify_base_url: str, certificate_code: str) -> str:
    clean_base = verify_base_url.rstrip("/")
    return (
        f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data="
        f"{quote(f'{clean_base}/assessments/verify/{certificate_code}/', safe='')}"
    )


def grade_quiz_submission(user, quiz: Quiz, submitted_answers: dict[int, str], verify_base_url: str = "https://skillscontinua-hosting-1.onrender.com"):
    """
    Grades a Quiz submission ({question_id: 'A'|'B'|'C'|'D'}), updates UserProgress,
    and issues/updates a Certificate (and CompetencyTranscript on Tier 3 pass) if passing.
    """
    questions = list(quiz.questions.order_by("order", "id"))
    total_questions = len(questions)
    correct_count = 0
    results = []

    for q in questions:
        chosen = (submitted_answers.get(q.id) or "").strip().upper()
        is_correct = chosen == q.correct_answer
        if is_correct:
            correct_count += 1
        results.append(
            {
                "question_id": q.id,
                "order": q.order,
                "chosen": chosen,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation,
            }
        )

    score_pct = round((correct_count / total_questions) * 100.0, 1) if total_questions else 0.0
    passed = score_pct >= quiz.passing_score_percentage
    grade_label = classify_grade(score_pct)

    certificate = None
    transcript = None

    if passed and quiz.trade_course:
        course = quiz.trade_course
        progress, _ = UserProgress.objects.get_or_create(user=user, trade_course=course)

        total_lessons = sum(m.lessons.count() for m in course.modules.all())
        completed_lessons = progress.completed_lessons.filter(module__trade_course=course).count()
        lesson_pct = (completed_lessons / total_lessons * 100.0) if total_lessons else 0.0
        progress.overall_progress_percentage = round(max(progress.overall_progress_percentage, min(100.0, lesson_pct if total_lessons else score_pct)), 1)

        if quiz.tier == "tier_1":
            progress.tier_1_completed = True
        elif quiz.tier == "tier_2":
            progress.tier_2_completed = True
        elif quiz.tier == "tier_3":
            progress.tier_3_completed = True
            progress.overall_progress_percentage = 100.0

        progress.last_activity = timezone.now()
        progress.save()

        cert_code = generate_verification_code("CERT", user.id, course.id, quiz.tier)
        existing_cert = Certificate.objects.filter(
            user=user, trade_course=course, tier=quiz.tier, is_revoked=False
        ).first()

        summary_text = (
            f"Course: {course.title} | Tier: {quiz.get_tier_display()} | "
            f"Assessment: {quiz.title} | Score: {score_pct}% ({correct_count}/{total_questions}) | "
            f"Classification: {grade_label}"
        )

        if existing_cert:
            if score_pct >= existing_cert.final_score:
                existing_cert.final_score = score_pct
                existing_cert.grade_classification = grade_label
                existing_cert.performance_summary = summary_text
                existing_cert.save()
            certificate = existing_cert
        else:
            certificate = Certificate.objects.create(
                user=user,
                trade_course=course,
                tier=quiz.tier,
                certificate_code=cert_code,
                final_score=score_pct,
                grade_classification=grade_label,
                performance_summary=summary_text,
                qr_code_url=build_qr_verification_url(verify_base_url, cert_code),
            )

        if quiz.tier == "tier_3":
            transcript_code = generate_verification_code("TRN", user.id, course.id, "transcript")
            competencies_list = "\n".join(
                f"- {mod.title}: {', '.join(les.title for les in mod.lessons.all())}"
                for mod in course.modules.all()
            )
            transcript, _ = CompetencyTranscript.objects.update_or_create(
                user=user,
                trade_course=course,
                defaults={
                    "certificate": certificate,
                    "transcript_code": transcript_code,
                    "total_hours_completed": course.duration_hours,
                    "tier_3_score": score_pct,
                    "verified_competencies": competencies_list or course.description,
                    "instructor_or_system_remarks": (
                        f"Verified completion of {course.title} with {score_pct}% ({grade_label})."
                    ),
                },
            )

    return {
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "tier": quiz.tier,
        "score_percentage": score_pct,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "passing_score_percentage": quiz.passing_score_percentage,
        "passed": passed,
        "grade_classification": grade_label,
        "results": results,
        "certificate": certificate,
        "transcript": transcript,
    }