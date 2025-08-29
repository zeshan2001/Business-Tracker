from django.shortcuts import render
from main_app.models import Bank
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
from main_app.models import Request, Business, Loan
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from datetime import date
from dateutil.relativedelta import relativedelta
from .forms import LoanForm
# Create your views here.
@role_required(allowed_roles=["L"])
def bank(request):
    profile = getattr(request.user, "profile", None)
    bank = Bank.objects.get(id= profile.bank_id)
    return render(request, "bank.html", {"bank": bank})

def request_view(request):
    bank_requests = Request.objects.filter(bank= request.user.profile.bank)

    return render(request, "request.html", {"requests": bank_requests})

def request_detail(request, request_id):
    bank_request = Request.objects.get(id = request_id)
    return render(request, "request_detail.html", {"request": bank_request})

class LoanCreate(CreateView):
    model = Loan
    form_class = LoanForm
    success_url = "/bank/"
    template_name = "loan.html"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        bank = self.request.user.profile.bank
        qs = Business.objects.filter(request__bank=bank).distinct()

        form.fields["business"].queryset = qs
        if not qs.exists():
            form.fields["business"].disabled = True
            form.fields["business"].empty_label = "No businesses with requests"

        return form

    def form_valid(self, form):
        if "business" not in form.fields:
            form.add_error(None, "No businesses have made requests yet.")
        form.instance.bank = self.request.user.profile.bank

        form.instance.start_date = date.today()

        years = int(form.cleaned_data["duration"])
        form.instance.end_date = date.today() + relativedelta(years=years)
        return super().form_valid(form)