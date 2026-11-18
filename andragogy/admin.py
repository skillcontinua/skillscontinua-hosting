from django.contrib import admin
from .models import AndragogicCourse, AndragogicModule, AndragogicLesson

admin.site.register(AndragogicCourse)
admin.site.register(AndragogicModule)
admin.site.register(AndragogicLesson)
