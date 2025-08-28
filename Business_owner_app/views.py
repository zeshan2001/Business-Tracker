from django.shortcuts import render,get_object_or_404
from main_app.models import Business ,Income_statement,Balance_sheet
from django.views.generic.edit import UpdateView,CreateView,DeleteView
# Create your views here.





class business_Create(CreateView):
    model=Business
    fields=['brand','init_cost', 'image', 'description']
    success_url='/business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class business_Updata(UpdateView):
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
    fields = ['revenue', 'cogs', 'operating_expenses', 'net_income', 'year']
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
    

class balance_sheet_Update(UpdateView):
    model = Balance_sheet
    fields = ['current_assets', 'non_current_assets', 'cash_equivalents', 'current_liabilities','non_current_liabilities','shareholders_equity', 'year']
    success_url = '/business/'


class balance_sheet_Delete(DeleteView):
    model = Balance_sheet
    success_url = '/business/'
   
    
    def form_valid(self, form):
        # Set the business from URL if provided
        business_id = self.kwargs.get('business_id')
        if business_id:
            form.instance.business = Business.objects.get(id=business_id)
        return super().form_valid(form)
    
    
def business(request):
    businesses=Business.objects.all()
    return render(request, 'business.html',{'businesses':businesses})

# def business_detail(request, business_id):
#     business = get_object_or_404(Business, id=business_id)
#     balance_sheets = business.balance_sheets.all()  
#     income_statements = business.income_statements.all()
#     context = {
#         'business': business,
#         'balance_sheets': balance_sheets,
#         'income_statements': income_statements,
#     }
#     return render(request, 'business_detail.html', context)





def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    
    # Get and sort financial data by year (most recent first)
    balance_sheets = business.balance_sheets.all().order_by('-year')
    income_statements = business.income_statements.all().order_by('-year')
    
    context = {
        'business': business,
        'balance_sheets': balance_sheets,
        'income_statements': income_statements,
    }
    return render(request, 'business_detail.html', context)

def profile(request):
    return render(request,'profile.html')