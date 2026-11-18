from django.contrib import admin
from .models import CybergogicCourse, CybergogicModule, CybergogicLesson

admin.site.register(CybergogicCourse)
admin.site.register(CybergogicModule)
admin.site.register(CybergogicLesson)
