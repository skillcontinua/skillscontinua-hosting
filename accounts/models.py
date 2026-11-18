# File path: C:\hosting\skillscontinua_hosting\accounts\models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('ig', 'Igbo'),
        ('sw', 'Swahili'),
        ('ar', 'Arabic'),
        ('es', 'Spanish'),
        ('pt', 'Portuguese')
    ]
    
    preferred_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Mobile number for SMS/Low-data support")
    is_mentor = models.BooleanField(default=False)
    is_corporate_partner = models.BooleanField(default=False)
    region_location = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Aba, Lagos, Nairobi")

    def __str__(self):
        return f"{self.username} ({self.email})"