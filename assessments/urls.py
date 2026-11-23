# File path: C:\hosting\skillscontinua_hosting\assessments\urls.py
from django.urls import path
from . import views

app_name = "assessments"

urlpatterns = [
    path("quiz/", views.quiz_list_view, name="quiz_list"),
    path("quiz/<int:quiz_id>/", views.quiz_submit_view, name="quiz_submit"),
    path("verify/", views.verify_lookup_view, name="verify_lookup"),
    path("verify/<str:code>/", views.verify_credential_view, name="verify_credential"),
]