from django.contrib import admin
from .models import PedagogicCourse, PedagogicModule, PedagogicLesson

admin.site.register(PedagogicCourse)
admin.site.register(PedagogicModule)
admin.site.register(PedagogicLesson)
