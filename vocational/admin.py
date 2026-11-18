from django.contrib import admin
from .models import TradeCategory, TradeCourse, TradeModule, TradeLesson

class TradeLessonInline(admin.TabularInline):
    model = TradeLesson
    extra = 1

class TradeModuleAdmin(admin.ModelAdmin):
    inlines = [TradeLessonInline]

admin.site.register(TradeCategory)
admin.site.register(TradeCourse)
admin.site.register(TradeModule, TradeModuleAdmin)
admin.site.register(TradeLesson)