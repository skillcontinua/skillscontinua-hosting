# File path: C:\hosting\skillscontinua_hosting\vocational\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import (
    TradeCategory,
    TradeCourse,
    TradeModule,
    TradeLesson,
    TradeGlossaryTerm,
)


class TradeCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


class TradeCourseTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
        "credential_awarded",
        "required_tools",
        "safety_guidelines",
        "field_tips_summary",
        "course_glossary_overview",
    )


class TradeModuleTranslationOptions(TranslationOptions):
    fields = ("title", "summary")


class TradeLessonTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "learning_objectives",
        "why_it_matters",
        "core_explanation",
        "step_by_step_field_guide",
        "safety_and_traps",
        "diagram_or_visual_guide",
        "real_life_scenario",
        "practice_activity",
        "checkpoint_questions",
    )


class TradeGlossaryTermTranslationOptions(TranslationOptions):
    fields = ("term", "full_expansion", "definition", "field_application")


translator.register(TradeCategory, TradeCategoryTranslationOptions)
translator.register(TradeCourse, TradeCourseTranslationOptions)
translator.register(TradeModule, TradeModuleTranslationOptions)
translator.register(TradeLesson, TradeLessonTranslationOptions)
translator.register(TradeGlossaryTerm, TradeGlossaryTermTranslationOptions)