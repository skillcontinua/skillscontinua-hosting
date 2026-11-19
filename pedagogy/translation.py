# File path: C:\hosting\skillscontinua_hosting\pedagogy\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import PedagogicCourse

class PedagogicCourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(PedagogicCourse, PedagogicCourseTranslationOptions)