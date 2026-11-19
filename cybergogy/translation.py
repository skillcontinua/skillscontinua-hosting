# File path: C:\hosting\skillscontinua_hosting\cybergogy\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import CybergogicCourse

class CybergogicCourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(CybergogicCourse, CybergogicCourseTranslationOptions)