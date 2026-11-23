# File path: C:\hosting\skillscontinua_hosting\assessments\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import Quiz, Question


class QuizTranslationOptions(TranslationOptions):
    fields = ("title", "instructions")


class QuestionTranslationOptions(TranslationOptions):
    fields = ("text", "option_a", "option_b", "option_c", "option_d", "explanation")


translator.register(Quiz, QuizTranslationOptions)
translator.register(Question, QuestionTranslationOptions)