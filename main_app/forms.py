from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only Business Owner + Investor
        self.fields["role"].choices = [
            ("B", "Business Owner"),
            ("I", "Investor"),
        ]