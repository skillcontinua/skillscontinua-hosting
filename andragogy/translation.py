# File path: C:\hosting\skillscontinua_hosting\andragogy\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import AndragogicCourse

class AndragogicCourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(AndragogicCourse, AndragogicCourseTranslationOptions)