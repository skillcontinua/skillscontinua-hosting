from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Non-translated global endpoints (Admin panel and language switcher selector)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Localized/Translated URL patterns for your 7 languages
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('pedagogy/', include('pedagogy.urls')),
    path('andragogy/', include('andragogy.urls')),
    path('heutagogy/', include('heutagogy.urls')),
    path('cybergogy/', include('cybergogy.urls')),
    path('vocational/', include('vocational.urls')),
    path('village/', include('village.urls')),
    path('assessments/', include('assessments.urls')),
    prefix_default_language=False,
)

# Media files routing for local testing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)