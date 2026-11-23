# File path: C:\hosting\skillscontinua_hosting\assessments\views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Quiz, Certificate, CompetencyTranscript
from .services import grade_quiz_submission


def quiz_list_view(request):
    quizzes = Quiz.objects.select_related("trade_course").order_by("trade_course__title", "tier", "id")
    return render(request, "assessments/quiz_list.html", {"quizzes": quizzes})


@login_required
def quiz_submit_view(request, quiz_id: int):
    quiz = get_object_or_404(
        Quiz.objects.prefetch_related("questions"), pk=quiz_id
    )
    questions = list(quiz.questions.order_by("order", "id"))
    grading_result = None

    if request.method == "POST":
        submitted_answers = {}
        for question in questions:
            val = request.POST.get(f"question_{question.id}")
            if val:
                submitted_answers[question.id] = val.strip().upper()

        verify_base_url = request.build_absolute_uri("/").rstrip("/")
        grading_result = grade_quiz_submission(
            user=request.user,
            quiz=quiz,
            submitted_answers=submitted_answers,
            verify_base_url=verify_base_url,
        )

    return render(
        request,
        "assessments/quiz_detail.html",
        {
            "quiz": quiz,
            "questions": questions,
            "grading_result": grading_result,
        },
    )


def verify_lookup_view(request):
    code = (request.GET.get("code") or "").strip().upper()
    if code:
        return redirect("assessments:verify_credential", code=code)
    return render(
        request,
        "assessments/verify_credential.html",
        {
            "code": "",
            "certificate": None,
            "transcript": None,
            "is_valid": False,
        },
    )


def verify_credential_view(request, code: str):
    normalized_code = code.strip().upper()
    certificate = (
        Certificate.objects.select_related("user", "trade_course")
        .filter(certificate_code__iexact=normalized_code)
        .first()
    )
    transcript = None

    if certificate:
        transcript = CompetencyTranscript.objects.filter(certificate=certificate).first()
    else:
        transcript = (
            CompetencyTranscript.objects.select_related("user", "trade_course", "certificate")
            .filter(transcript_code__iexact=normalized_code)
            .first()
        )
        if transcript and transcript.certificate:
            certificate = transcript.certificate

    is_valid = bool(certificate and not certificate.is_revoked) or bool(transcript and not certificate)

    return render(
        request,
        "assessments/verify_credential.html",
        {
            "code": normalized_code,
            "certificate": certificate,
            "transcript": transcript,
            "is_valid": is_valid,
        },
    )