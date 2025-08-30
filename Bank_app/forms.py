from django import forms
from main_app.models import Loan, Request
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

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["status"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            ("A", "Accepted"),
            ("R", "Rejected")
        ]