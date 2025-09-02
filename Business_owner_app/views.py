from django.shortcuts import render,get_object_or_404, redirect
from main_app.models import Business ,Income_statement,Balance_sheet,Bank,Request, Profile, Loan
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.urls import reverse_lazy
import numpy_financial as npf
from django.contrib.auth import update_session_auth_hash
from django.views import View
from main_app.forms import ProfileForm
from django.contrib.auth.models import User
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin

# Create your views here.

class business_Create(RoleRequiredMixin ,CreateView):
    allowed_roles= ["B"]
    model=Business
    fields=['brand','init_cost', 'image', 'description']
    success_url='/business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class business_Update(RoleRequiredMixin,UpdateView):
    allowed_roles= ["B"]
    model=Business
    fields=['brand','init_cost', 'image', 'description']
    success_url='/business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")


class business_Delete(RoleRequiredMixin,DeleteView):
    allowed_roles= ["B"]
    model=Business
    success_url='/business/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

class income_statement(RoleRequiredMixin,CreateView):
    allowed_roles= ["B"]
    model = Income_statement
    fields = ['revenue', 'non_cash_expense', 'cogs', 'operating_expenses', 'net_income', 'year']

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy("business_detail", kwargs={"business_id": obj.business.id})

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the business field from URL parameter
        business_id = self.kwargs.get('business_id')
        if business_id:
            initial['business'] = Business.objects.get(id=business_id)
        return initial
    
    def form_valid(self, form):
        # Set the business from URL if provided
        business_id = self.kwargs.get('business_id')
        if business_id:
            form.instance.business = Business.objects.get(id=business_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("business_detail", kwargs={"business_id": self.object.business.id })


class balance_sheet(RoleRequiredMixin ,CreateView):
    allowed_roles= ["B"]
    model = Balance_sheet
    fields = ['current_assets', 'non_current_assets', 'cash_equivalents', 'current_liabilities','non_current_liabilities','shareholders_equity', 'year']

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the business field from URL parameter
        business_id = self.kwargs.get('business_id')
        if business_id:
            initial['business'] = Business.objects.get(id=business_id)
        return initial
    
    def form_valid(self, form):
        # Set the business from URL if provided
        business_id = self.kwargs.get('business_id')
        if business_id:
            form.instance.business = Business.objects.get(id=business_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("business_detail", kwargs={"business_id": self.object.business.id })
    
    

class balance_sheet_Update(RoleRequiredMixin,UpdateView):
    allowed_roles= ["B"]
    model = Balance_sheet
    fields = ['current_assets', 'non_current_assets', 'cash_equivalents', 'current_liabilities','non_current_liabilities','shareholders_equity', 'year']

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy("business_detail", kwargs={"business_id": obj.business.id})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        related_business = obj.business
        if related_business.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")


class balance_sheet_Delete(RoleRequiredMixin,DeleteView):
    allowed_roles= ["B"]
    model = Balance_sheet

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy("business_detail", kwargs={"business_id": obj.business.id})
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        related_business = obj.business
        if related_business.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")


class income_statement_Update(RoleRequiredMixin ,UpdateView):
    allowed_roles=["B"]
    model = Income_statement
    fields = ['revenue', 'non_cash_expense', 'cogs', 'operating_expenses', 'net_income', 'year']

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy("business_detail", kwargs={"business_id": obj.business.id})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        related_business = obj.business

        if related_business.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

class income_statement_Delete(RoleRequiredMixin ,DeleteView):
    allowed_roles=["B"]
    model = Income_statement

    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy("business_detail", kwargs={"business_id": obj.business.id})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        related_business = obj.business
        if related_business.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

@role_required(allowed_roles=["B"])
def list_Bank(request):
    listOfbanks=Bank.objects.all()
    return render(request,'list-banks.html',{'listOfbanks':listOfbanks})


class Create_Request(RoleRequiredMixin,CreateView):
    allowed_roles= ["B"]
    model = Request
    fields = ['borrow_amount', 'description',"business"]  # Only include fields the user should fill
    success_url = reverse_lazy('list-banks')
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the bank field from URL parameter
        bank_id = self.kwargs.get('bank_id')
        if bank_id:
            initial['bank'] = get_object_or_404(Bank, id=bank_id)
        return initial
    
    def get_form(self, form_class =None):
        form = super().get_form(form_class)
        qs = Business.objects.filter(user= self.request.user).exclude(request__isnull = False)

        form.fields["business"].queryset = qs
        if not qs.exists():
            form.fields["business"].disabled = True
            form.fields["business"].empty_label = "No businesses with requests"
        return form

    def form_valid(self, form):
        bank_id = self.kwargs.get('bank_id')
        bank = Bank.objects.filter(id= bank_id).first()
        form.instance.bank = bank
        form.instance.status = "P"
        
        return super().form_valid(form)

@role_required(allowed_roles=["B"])
def business(request):
    businesses=Business.objects.filter(user = request.user)
    return render(request, 'business.html',{'businesses':businesses})

@role_required(allowed_roles=["B"])

def loan_business(request):
    loan_business = Loan.objects.filter(business__user = request.user)
    print(f"loan_business:::::::: {loan_business}")
    return render(request, "loan_view.html", {"loans": loan_business})

@role_required(allowed_roles=["B"])
def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    
    
    # Get and sort financial data by year (most recent first)
    balance_sheets = business.balance_sheets.all().order_by('-year')
    income_statements = business.income_statements.all().order_by('-year')
    tvc = 0
    tfc = 0
    for inc in income_statements:
        tvc += inc.cogs
        tfc += inc.operating_expenses

    tc = tvc + tfc
    
    def payback_period():
        new_cost = business.init_cost * -1
        year = -1
        cash_flow = []

        reversed_statements_income = business.income_statements.all().order_by('year')
        if (income_statements):
            last_amount = reversed_statements_income.last().net_income
            for inc in reversed_statements_income:
                if new_cost <= 0:
                    new_cost += inc.net_income 
                    year+= 1
                    cash_flow.append(inc.net_income)

            last_amount = cash_flow[-1]
            if last_amount > 0:
                while new_cost <= 0:
                    new_cost += last_amount
                    year += 1
                    cash_flow.append(last_amount)
                prev_cost = new_cost - last_amount
                
                prev_cost = abs(prev_cost)
                year = round(year + (prev_cost/cash_flow[-1]))
        return year, cash_flow 
    year, cash_flow = payback_period()

    def npv(rate):
        discount_rate = rate
        sum_of_cash = 0
        for num in range(0, len(cash_flow)):
            sum_of_cash += float(cash_flow[num]) / float((1+discount_rate)**(num+1))
        npv_value = sum_of_cash - float(business.init_cost)
        return npv_value

    def irr():
        cash_flow_with_init = [-float(business.init_cost)] + [float(cf) for cf in cash_flow]
        irr = npf.irr(cash_flow_with_init)
        return irr

    irr_rate = irr()

    pie_labels = ["TVC", "TFC", "TC"]
    pie_data = [float(tvc), float(tfc), float(tc)]

    discount_rates = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    npv_values =  []
    for i in range(50, -5, -5):
        npv_values.append(npv(i/100))
    
    irr = irr_rate  # Example IRR

    sum_of_net_income = 0

    for income_statement in income_statements:
        sum_of_net_income += income_statement.net_income

    check_if_true = sum_of_net_income < 0

    # sum_of_npv_values =  < business.init_cost
    print( sum_of_net_income)
    context = {
        'business': business,
        'balance_sheets': balance_sheets,
        'income_statements': income_statements,
        "year": year,
        "pie_labels": pie_labels,
        "pie_data": pie_data,
        'discount_rates': discount_rates,
        'npv_values': npv_values,
        'irr': irr,
        "is_loss": check_if_true
    }
    return render(request, 'business_detail.html', context)


class ProfileDetail(RoleRequiredMixin,View):
    allowed_roles= ["B"]
    def get(self, request):
        owner = Profile.objects.get(user=request.user)
        return render(request, 'profile.html', {'owner': owner})

class ProfileUpdate(RoleRequiredMixin,UpdateView):
    allowed_roles=["B"]
    model = Profile
    fields = ['email', 'phone']
    template_name = 'profile_update.html'
    success_url = reverse_lazy('Profile')
    
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
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)


@role_required(allowed_roles=["B"])
def dashboard(request):
    user_income_statements = Income_statement.objects.select_related('business').filter(business__user=request.user)

    # aggregate by business
    business_data = {}
    yearly_data = {}
    for single in user_income_statements:
        year = single.year
        business = single.business.brand
        revenue = float(single.revenue)
        cost = float(single.cogs) + float(single.operating_expenses)

        # aggregate per year
        if year not in yearly_data:
            yearly_data[year] = {"revenue": 0.0, "cost": 0.0}
        yearly_data[year]["revenue"] += revenue
        yearly_data[year]["cost"] += cost

        # aggregate per business
        if business not in business_data:
            business_data[business] = {"revenue": 0.0, "cost": 0.0}
        business_data[business]["revenue"] += revenue
        business_data[business]["cost"] += cost

    # build yearly array
    revenue_cost_over_year = []
    for year, vals in yearly_data.items():
        revenue_cost_over_year.append({
            "year": year,
            "revenue": vals["revenue"],
            "cost": vals["cost"]
        })

    business_labels = list(business_data.keys())
    revenue_data = [vals["revenue"] for vals in business_data.values()]
    cost_data = [vals["cost"] for vals in business_data.values()]

    years = [single["year"] for single in revenue_cost_over_year]
    revenue = [single["revenue"] for single in revenue_cost_over_year]
    cost = [single["cost"] for single in revenue_cost_over_year]

    context = {
        "business_labels": business_labels,
        "revenue_data": revenue_data,
        "cost_data": cost_data,
        "years": years,
        "revenue": revenue,
        "cost": cost,
    }
    return render(request, 'dashboard.html', context)

