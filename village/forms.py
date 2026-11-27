# File path: C:\hosting\skillscontinua_hosting\village\forms.py
from django import forms
from .models import ForumReply


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ("message",)
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Share your experience, ask a follow-up, or help a fellow learner…",
            }),
        }
        labels = {"message": "Your reply"}

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 5:
            raise forms.ValidationError("Reply is too short — please add at least 5 characters.")
        if len(message) > 5000:
            raise forms.ValidationError("Reply is too long (max 5000 characters).")
        return message