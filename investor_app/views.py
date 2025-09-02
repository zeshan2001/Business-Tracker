from django.shortcuts import render,get_object_or_404, redirect
from main_app.decorators import role_required
from main_app.models import Business, Profile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views import View
from main_app.mixins import RoleRequiredMixin
import numpy_financial as npf

# Create your views here.

@role_required(allowed_roles=["I"])
def investor_dashborad(request):
    businesses = Business.objects.all()
    return render(request, "investor_dasborad.html", { 'businesses' : businesses })

class ProfileDetail(RoleRequiredMixin,View):
    allowed_roles = ["I"]
    def get(self, request):
        owner = Profile.objects.get(user=request.user)
        return render(request, 'Investor_Profile.html', {'owner': owner})

class ProfileUpdate(RoleRequiredMixin,UpdateView):
    model = Profile
    allowed_roles= ["I"]
    fields = ['email', 'phone']
    template_name = 'Investor_Profile_Update.html'
    success_url = reverse_lazy('Investor_Profile')
    
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


class ProfileDelete(RoleRequiredMixin ,View):
    allowed_roles= ["I"]
    def get(self, request):
        owner = get_object_or_404(Profile, user=request.user)
        return render(request, 'investor_profile_confirm_delete.html', {'owner': owner})

    def post(self, request):
        owner = get_object_or_404(Profile, user=request.user)
        user = owner.user   # grab linked auth.User
        owner.delete()      # delete profile
        user.delete()        # delete user
        return redirect('home')

@role_required(allowed_roles=["I"])
def investment_detail(request, business_id):
    business_id = Business.objects.get(id=business_id)
    owner = getattr(business_id.user, "profile", None)
    balance_sheets = business_id.balance_sheets.all().order_by('-year')
    income_statements = business_id.income_statements.all().order_by('-year')
    tvc = 0
    tfc = 0
    for inc in income_statements:
        tvc += inc.cogs
        tfc += inc.operating_expenses

    tc = tvc + tfc
    
    def payback_period():
        new_cost = business_id.init_cost * -1
        year = -1
        cash_flow = []

        reversed_statements_income = business_id.income_statements.all().order_by('year')
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
        npv_value = sum_of_cash - float(business_id.init_cost)
        return npv_value

    def irr():
        cash_flow_with_init = [-float(business_id.init_cost)] + [float(cf) for cf in cash_flow]
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

    # New data for User Businesses chart
    # Example: One user with multiple businesses
    context = {
        'business_id': business_id,
        'owner': owner,
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

    return render(request, "investment_detail.html", context)
