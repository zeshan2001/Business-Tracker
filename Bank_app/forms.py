from django import forms
from main_app.models import Loan

class LoanForm(forms.ModelForm):
    DURATION_CHOICES = [
        (3, "3 Years"),
        (5, "5 Years"),
        (7, "7 Years"),
    ]
    duration = forms.ChoiceField(choices=DURATION_CHOICES)

    class Meta:
        model = Loan
        fields = ["business", "loan_amount", "interest_rate", "duration"]