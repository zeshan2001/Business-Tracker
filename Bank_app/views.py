from django.shortcuts import render,get_object_or_404, redirect
from main_app.models import Request, Business, Loan, Balance_sheet, Income_statement, Profile, Bank
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import View
from datetime import date
from dateutil.relativedelta import relativedelta
from .forms import LoanForm, RequestForm
from django.urls import reverse_lazy 
from django.contrib.auth import update_session_auth_hash




# Create your views here.
@role_required(allowed_roles=["L"])
def bank(request):
    profile = getattr(request.user, "profile", None)
    bank = Bank.objects.get(id= profile.bank_id)
    return render(request, "bank.html", {"bank": bank})
@role_required(allowed_roles=["L"])
def request_view(request):
    bank_requests = Request.objects.filter(bank= request.user.profile.bank, status="P")
    return render(request, "request.html", {"requests": bank_requests})

@role_required(allowed_roles=["L"])
def request_detail(request, request_id):
    bank_request = Request.objects.get(id = request_id)
    balance_sheets = Balance_sheet.objects.filter(business= bank_request.business.id)
    income_statements = Income_statement.objects.filter(business= bank_request.business.id)
    income_statement = Income_statement.objects.filter(business= bank_request.business.id).order_by("-year").first()
    
    def debt_service_coverage_ratio():
        cash_available = income_statement.net_income + income_statement.non_cash_expense
        loan_payment = bank_request.borrow_amount
        dscr = cash_available / loan_payment
        return dscr
    dscr = debt_service_coverage_ratio()
    if request.user.profile.bank == bank_request.bank:
        return render(request, "request_detail.html", {"request": bank_request, "balance_sheets": balance_sheets, "income_statements": income_statements, "DSCR": dscr})
    else:
        return redirect("home")



class LoanCreate(RoleRequiredMixin,CreateView):
    allowed_roles = ["L"]
    model = Loan
    form_class = LoanForm
    success_url = "/bank/"
    template_name = "loan.html"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        bank = self.request.user.profile.bank
        qs = Business.objects.filter(request__bank=bank, request__status="A").distinct()

        qs = qs.exclude(loan__bank=bank)

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
    


class RequstDetail(RoleRequiredMixin,View):
    allowed_roles = ["L"]

    def get(self, request, business_id):
        bank_request = Request.objects.filter(
            business_id = business_id, bank= request.user.profile.bank
        ).first()
        if request.user.profile.bank == bank_request.bank:
            return render(request, "request_detail_loan.html", {"request": bank_request})
        else: 
            return redirect("home")



class RequestUpdate(RoleRequiredMixin,UpdateView):
    allowed_roles = ["L"]
    model = Request
    form_class = RequestForm
    template_name = "request_update.html"
    success_url = reverse_lazy("request")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.profile.bank != obj.bank:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_request"] = self.object
        return context


# Profile


class ProfileDetail(RoleRequiredMixin,View):
    allowed_roles = ["L"]
    def get(self, request):
        owner = Profile.objects.get(user=request.user)
        return render(request, 'Bank_Profile.html', {'owner': owner})

class ProfileUpdate(RoleRequiredMixin,UpdateView):
    allowed_roles = ["L"]
    model = Profile
    fields = []
    # fields = ['email', 'phone']
    template_name = 'Bank_Profile_Update.html'
    success_url = reverse_lazy('Bank_Profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        # Check if password was submitted in the request
        new_password = self.request.POST.get('password')
        if new_password:
            user = self.request.user
            user.set_password(new_password)  # hashes automatically
            user.save()
            # keep the user logged in after password change
            update_session_auth_hash(self.request, user)

        return response
