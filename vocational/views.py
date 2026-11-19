# File path: C:\hosting\skillscontinua_hosting\vocational\views.py
from django.shortcuts import render, get_object_or_404
from .models import TradeCourse, TradeLesson

def course_list_view(request):
    courses = TradeCourse.objects.all()
    context = {'courses': courses}
    return render(request, 'vocational/course_list.html', context)

def course_detail_view(request, slug):
    course = get_object_or_404(TradeCourse, slug=slug)
    context = {'course': course}
    return render(request, 'vocational/course_detail.html', context)

def lesson_detail_view(request, course_slug, lesson_id):
    course = get_object_or_404(TradeCourse, slug=course_slug)
    lesson = get_object_or_404(TradeLesson, id=lesson_id)
    context = {'course': course, 'lesson': lesson}
    return render(request, 'vocational/lesson_detail.html', context)