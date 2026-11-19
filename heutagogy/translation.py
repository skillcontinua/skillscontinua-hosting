# File path: C:\hosting\skillscontinua_hosting\heutagogy\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import HeutagogicCourse

class HeutagogicCourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(HeutagogicCourse, HeutagogicCourseTranslationOptions)