# File path: C:\hosting\skillscontinua_hosting\vocational\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import TradeCourse

class TradeCourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'required_tools', 'safety_guidelines')

translator.register(TradeCourse, TradeCourseTranslationOptions)