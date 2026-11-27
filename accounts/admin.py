# File path: C:\hosting\skillscontinua_hosting\accounts\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "preferred_language",
        "region_location", "is_mentor", "is_staff",
    )
    list_filter = UserAdmin.list_filter + ("is_mentor", "is_corporate_partner", "preferred_language")

    fieldsets = UserAdmin.fieldsets + (
        ("SkillsContinua Custom Fields", {
            "fields": (
                "preferred_language", "phone_number",
                "is_mentor", "is_corporate_partner", "region_location",
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("SkillsContinua Custom Fields", {
            "fields": (
                "preferred_language", "phone_number",
                "is_mentor", "is_corporate_partner", "region_location",
            ),
        }),
    )