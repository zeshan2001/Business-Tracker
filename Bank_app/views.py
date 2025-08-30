from django.shortcuts import render
from main_app.models import Bank
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
from main_app.models import Request, Business, Loan, Balance_sheet, Income_statement
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from datetime import date
from dateutil.relativedelta import relativedelta
from .forms import LoanForm, RequestForm
from django.urls import reverse_lazy
# Create your views here.
@role_required(allowed_roles=["L"])
def bank(request):
    profile = getattr(request.user, "profile", None)
    bank = Bank.objects.get(id= profile.bank_id)
    return render(request, "bank.html", {"bank": bank})

def request_view(request):
    bank_requests = Request.objects.filter(bank= request.user.profile.bank, status="P")
    return render(request, "request.html", {"requests": bank_requests})

def request_detail(request, request_id):
    bank_request = Request.objects.get(id = request_id)
    balance_sheets = Balance_sheet.objects.filter(business= bank_request.business.id)
    income_statements = Income_statement.objects.filter(business= bank_request.business.id)
    income_statement = Income_statement.objects.filter(business= bank_request.business.id).order_by("-year").first()
    print(income_statement)
    
    def debt_service_coverage_ratio():
        cash_available = income_statement.net_income + income_statement.non_cash_expense
        loan_payment = bank_request.borrow_amount
        dscr = cash_available / loan_payment
        return dscr
    dscr = debt_service_coverage_ratio()


    return render(request, "request_detail.html", {"request": bank_request, "balance_sheets": balance_sheets, "income_statements": income_statements, "DSCR": dscr})


class LoanCreate(CreateView):
    model = Loan
    form_class = LoanForm
    success_url = "/bank/"
    template_name = "loan.html"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        bank = self.request.user.profile.bank
        qs = Business.objects.filter(request__bank=bank, request__status="P").distinct()

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

class RequestUpdate(UpdateView):
    model = Request
    form_class = RequestForm
    template_name = "request_update.html"
    success_url = reverse_lazy("request")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_request"] = self.object
        return context
    
