from django.contrib import admin
from .models import Quiz, Question, UserProgress, Certificate, DropoutTestimonial

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(UserProgress)
admin.site.register(Certificate)
admin.site.register(DropoutTestimonial)