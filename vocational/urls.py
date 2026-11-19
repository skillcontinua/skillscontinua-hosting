# File path: C:\hosting\skillscontinua_hosting\vocational\urls.py
from django.urls import path
from .views import course_list_view, course_detail_view, lesson_detail_view

app_name = 'vocational'

urlpatterns = [
    path('', course_list_view, name='course_list'),
    path('<slug:slug>/', course_detail_view, name='course_detail'),
    path('<slug:course_slug>/lesson/<int:lesson_id>/', lesson_detail_view, name='lesson_detail'),
]