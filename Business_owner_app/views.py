from django.shortcuts import render,get_object_or_404, redirect
from main_app.models import Business ,Income_statement,Balance_sheet,Bank,Request, Profile
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.urls import reverse_lazy
import numpy_financial as npf
from django.contrib.auth import update_session_auth_hash
from django.views import View

from main_app.forms import ProfileForm
from django.contrib.auth.models import User

# Create your views here.

class business_Create(CreateView):
    model=Business
    fields=['brand','init_cost', 'image', 'description']
    success_url='/business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class business_Update(UpdateView):
    model=Business
    fields=['brand','init_cost', 'image', 'description']
    success_url='/business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class business_Delete(DeleteView):
    model=Business
    success_url='/business/'

class income_statement(CreateView):
    model = Income_statement
    fields = ['revenue', 'non_cash_expense', 'cogs', 'operating_expenses', 'net_income', 'year']
    success_url = '/business/'
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
    
class balance_sheet(CreateView):
    model = Balance_sheet
    fields = ['current_assets', 'non_current_assets', 'cash_equivalents', 'current_liabilities','non_current_liabilities','shareholders_equity', 'year']
    success_url = '/business/'
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
    

class balance_sheet_Update(UpdateView):
    model = Balance_sheet
    fields = ['current_assets', 'non_current_assets', 'cash_equivalents', 'current_liabilities','non_current_liabilities','shareholders_equity', 'year']
    success_url = '/business/'


class balance_sheet_Delete(DeleteView):
    model = Balance_sheet
    success_url = '/business/'


class income_statement_Update(UpdateView):
    model = Income_statement
    fields = ['revenue', 'non_cash_expense', 'cogs', 'operating_expenses', 'net_income', 'year']
    success_url = '/business/'

class income_statement_Delete(DeleteView):
    model = Income_statement
    success_url = '/business/'


def list_Bank(request):
    listOfbanks=Bank.objects.all()
    return render(request,'list-banks.html',{'listOfbanks':listOfbanks})


class Create_Request(CreateView):
    model = Request
    fields = ['borrow_amount', 'description']  # Only include fields the user should fill
    success_url = reverse_lazy('list-banks')
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the bank field from URL parameter
        bank_id = self.kwargs.get('bank_id')
        if bank_id:
            initial['bank'] = get_object_or_404(Bank, id=bank_id)
        return initial
    
    def form_valid(self, form):
        # Set the business from the current user
        user_business = get_object_or_404(Business, user=self.request.user)
        form.instance.business = user_business
        
        # Set the bank from URL parameter
        bank_id = self.kwargs.get('bank_id')
        if bank_id:
            form.instance.bank = get_object_or_404(Bank, id=bank_id)
        
        # Always set status to "P" (Pending)
        form.instance.status = "P"
        
        return super().form_valid(form)



def business(request):
    businesses=Business.objects.filter(user = request.user)
    return render(request, 'business.html',{'businesses':businesses})




def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    
    
    # Get and sort financial data by year (most recent first)
    balance_sheets = business.balance_sheets.all().order_by('-year')
    income_statements = business.income_statements.all().order_by('-year')
    
    def payback_period():
        new_cost = business.init_cost * -1
        year = -1
        cash_flow = []
        # discount_rate = 0.05
        reversed_statements_income = business.income_statements.all().order_by('year')
        if (income_statements):
            last_amount = reversed_statements_income.last().net_income
            for inc in reversed_statements_income:
                if new_cost <= 0:
                    new_cost += inc.net_income 
                    year+= 1
                    cash_flow.append(inc.net_income)

                last_amount = cash_flow[-1]
            while new_cost <= 0:
                new_cost += last_amount
                year += 1
                cash_flow.append(last_amount)
            prev_cost = new_cost - last_amount
            
            prev_cost = abs(prev_cost)
            year = round(year + (prev_cost/cash_flow[-1]))
        return year, cash_flow 
    year, cash_flow = payback_period()

    def npv():
        discount_rate = 0.05
        sum_of_cash = 0
        for num in range(0, len(cash_flow)):
            sum_of_cash += float(cash_flow[num]) / float((1+discount_rate)**(num+1))
            print(cash_flow[num])
            print(sum_of_cash)
        npv_value = sum_of_cash - float(business.init_cost)
        return npv_value
    
    npv_value = npv()
    print(f"this is npv value {npv_value}")
    # print(year)
    print(cash_flow)

    def irr():
        
        cash_flow_with_init = [-float(business.init_cost)] + [float(cf) for cf in cash_flow]
        irr = npf.irr(cash_flow_with_init)
        return irr

    irr_rate = irr()
    print(irr_rate)

        # npv_value = ( / discount_factor) - float(business.init_cost)
        # print((float(discount_factor)/float(sum_new_cost)) - float(10000))
    # Income_statement = getattr(business2, "income_statement", None)
    # print(Income_statement)
    context = {
        'business': business,
        'balance_sheets': balance_sheets,
        'income_statements': income_statements,
        "year": year
    }
    return render(request, 'business_detail.html', context)


class ProfileDetail(View):

    def get(self, request):
        owner = Profile.objects.get(user=request.user)
        return render(request, 'profile.html', {'owner': owner})

class ProfileUpdate(UpdateView):
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


class ProfileDelete(View):
    def get(self, request):
        owner = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile_confirm_delete.html', {'owner': owner})

    def post(self, request):
        owner = get_object_or_404(Profile, user=request.user)
        user = owner.user   # grab linked auth.User
        owner.delete()      # delete profile
        user.delete()        # delete user
        return redirect('home')  