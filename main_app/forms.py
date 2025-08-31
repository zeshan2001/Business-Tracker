from django import forms
from .models import Profile
from django import forms
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role", "email","phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only Business Owner + Investor
        self.fields["role"].choices = [
            ("B", "Business Owner"),
            ("I", "Investor"),
        ]

class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)