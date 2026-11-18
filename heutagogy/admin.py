from django.contrib import admin
from .models import HeutagogicCourse, HeutagogicModule, HeutagogicLesson

admin.site.register(HeutagogicCourse)
admin.site.register(HeutagogicModule)
admin.site.register(HeutagogicLesson)
