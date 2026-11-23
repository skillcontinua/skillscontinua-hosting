# File path: C:\hosting\skillscontinua_hosting\vocational\views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from assessments.models import Certificate, Quiz, UserProgress
from .models import TradeCategory, TradeCourse, TradeLesson


def _user_has_course_access(request, course: TradeCourse) -> bool:
    """
    Tier 1 (is_free_tier=True) is open to everyone as an appetite-building entry track.
    Tier 2 and Tier 3 unlock for staff/instructors, corporate partners, enrolled learners
    (UserProgress/Certificate), or session-unlocked preview codes.
    """
    if course.is_free_tier or course.tier == "tier_1":
        return True

    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        if user.is_staff or user.is_superuser or getattr(user, "is_corporate_partner", False):
            return True
        if UserProgress.objects.filter(
            user=user, trade_course=course, is_active_student=True
        ).exists():
            return True
        if Certificate.objects.filter(
            user=user, trade_course=course, is_revoked=False
        ).exists():
            return True

    unlocked_slugs = request.session.get("unlocked_trade_courses", [])
    return course.slug in unlocked_slugs


def _sync_user_language(request):
    """Sync active language with authenticated user's preferred_language if no session override exists."""
    user = getattr(request, "user", None)
    if (
        user
        and user.is_authenticated
        and not request.session.get("_language")
        and getattr(user, "preferred_language", None)
    ):
        translation.activate(user.preferred_language)
        request.LANGUAGE_CODE = user.preferred_language


def course_list_view(request):
    _sync_user_language(request)
    categories = TradeCategory.objects.prefetch_related(
        "trade_courses__modules__lessons",
        "trade_courses__quizzes",
    ).all()

    tracks = []
    for category in categories:
        cat_courses = list(category.trade_courses.all())
        tier_map = {c.tier: c for c in cat_courses}
        tracks.append(
            {
                "category": category,
                "tier_1": tier_map.get("tier_1"),
                "tier_2": tier_map.get("tier_2"),
                "tier_3": tier_map.get("tier_3"),
                "courses": cat_courses,
            }
        )

    context = {
        "tracks": tracks,
        "courses": TradeCourse.objects.select_related("category").all(),
    }
    return render(request, "vocational/course_list.html", context)


def course_detail_view(request, slug):
    _sync_user_language(request)
    course = get_object_or_404(
        TradeCourse.objects.select_related("category").prefetch_related(
            "modules__lessons",
            "glossary_terms",
            "quizzes",
        ),
        slug=slug,
    )

    if request.method == "POST" and request.POST.get("action") == "unlock_tier":
        if not request.user.is_authenticated:
            messages.info(
                request,
                "Sign in or create a free learner account first to enroll in Tier 2 and Tier 3 tracks.",
            )
            return redirect("vocational:course_detail", slug=course.slug)

        UserProgress.objects.get_or_create(
            user=request.user,
            trade_course=course,
            defaults={"is_active_student": True},
        )
        messages.success(
            request,
            f"Enrollment activated for {course.title}. Full field manuals and assessments are now unlocked.",
        )
        return redirect("vocational:course_detail", slug=course.slug)

    has_access = _user_has_course_access(request, course)
    sibling_courses = list(
        TradeCourse.objects.filter(category=course.category).order_by("tier", "title")
    )
    quizzes = Quiz.objects.filter(trade_course=course).order_by("tier", "id")

    context = {
        "course": course,
        "has_access": has_access,
        "sibling_courses": sibling_courses,
        "quizzes": quizzes,
    }
    return render(request, "vocational/course_detail.html", context)


def lesson_detail_view(request, course_slug, lesson_id):
    _sync_user_language(request)
    course = get_object_or_404(TradeCourse.objects.select_related("category"), slug=course_slug)
    lesson = get_object_or_404(
        TradeLesson.objects.select_related("module"),
        id=lesson_id,
        module__trade_course=course,
    )

    has_course_access = _user_has_course_access(request, course)
    can_view_lesson = has_course_access or lesson.is_free_preview

    course_lessons = list(
        TradeLesson.objects.filter(module__trade_course=course).order_by(
            "module__order", "order", "id"
        )
    )
    prev_lesson = None
    next_lesson = None
    for idx, item in enumerate(course_lessons):
        if item.id == lesson.id:
            if idx > 0:
                prev_lesson = course_lessons[idx - 1]
            if idx + 1 < len(course_lessons):
                next_lesson = course_lessons[idx + 1]
            break

    context = {
        "course": course,
        "lesson": lesson,
        "has_course_access": has_course_access,
        "can_view_lesson": can_view_lesson,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
    }
    return render(request, "vocational/lesson_detail.html", context)