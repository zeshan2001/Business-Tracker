from django.shortcuts import render,get_object_or_404
from main_app.models import Business ,Income_statement,Balance_sheet
from django.views.generic.edit import UpdateView,CreateView,DeleteView
import numpy_financial as npf
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


class income_statement_Updata(UpdateView):
    model = Income_statement
    fields = ['revenue', 'non_cash_expense', 'cogs', 'operating_expenses', 'net_income', 'year']
    success_url = '/business/'

class income_statement_Delete(DeleteView):
    model = Income_statement
    success_url = '/business/'

    
def business(request):
    businesses=Business.objects.filter(user = request.user)
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

    def npv(rate):
        discount_rate = rate
        sum_of_cash = 0
        for num in range(0, len(cash_flow)):
            sum_of_cash += float(cash_flow[num]) / float((1+discount_rate)**(num+1))
            print(cash_flow[num])
            print(sum_of_cash)
        npv_value = sum_of_cash - float(business.init_cost)
        return npv_value

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
    # Sample data
    # bar_labels = ["Jan", "Feb", "Mar", "Apr", "May"]
    # bar_data = [10, 20, 30, 40, 50]

    pie_labels = ["TVC", "TFC", "TC"]
    pie_data = [float(tvc), float(tfc), float(tc)]
    # pie_data = [6, 6, 6]
    print(f"ddddddd::: {pie_labels}")
    print(f"fffffffffffffffffff::: {pie_data}")

    # line_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
    # line_data = [5, 15, 10, 20]

    discount_rates = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    npv_values =  []
    for i in range(50, -5, -5):
        npv_values.append(npv(i/100))
    
    print(f"npv_values::: {npv_values}")

    irr = irr_rate  # Example IRR
    print(f"rr_rate / 5::: {irr}")

    # New data for User Businesses chart
    # Example: One user with multiple businesses
    business_labels = ["Business A", "Business B", "Business C"]
    revenue_data = [15000, 22000, 18000]
    cost_data = [9000, 14000, 12000]
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
        'business_labels': business_labels,
        'revenue_data': revenue_data,
        'cost_data': cost_data,
    }
    return render(request, 'business_detail.html', context)

def profile(request):
    return render(request,'profile.html')


def dashboard(request):
    user_income_statements = Income_statement.objects.select_related('business').filter(business__user=request.user)

    # New data for User Businesses chart
    # Example: One user with multiple businesses
    business_labels = []
    revenue_data = []
    years_array = []
    cost_data = []
    revenue_cost_over_year = []

    # temporary dict to sum values per year
    yearly_data = {}

    for single in user_income_statements:
        year = single.year
        revenue = float(single.revenue)
        cost = float(single.cogs) + float(single.operating_expenses)

        business_labels.append(single.business.brand)
        revenue_data.append(revenue)
        cost_data.append(cost)
        years_array.append(year)

        # aggregate by year
        if year not in yearly_data:
            yearly_data[year] = {"revenue": 0.0, "cost": 0.0}
        yearly_data[year]["revenue"] += revenue
        yearly_data[year]["cost"] += cost

    # now build the final sss array (aggregated)
    for year, vals in yearly_data.items():
        revenue_cost_over_year.append({
            "year": year,
            "revenue": vals["revenue"],
            "cost": vals["cost"]
        })
    print(f"sss::: {revenue_cost_over_year}")
    # [{'year': '2022', 'revenue': 10250000.0, 'cost': 184586.0}, {'year': '2023', 'revenue': 32124.0, 'cost': 739.0}]


    # Example: revenue and cost across years
    years = []
    revenue = []
    cost = []
    for single in revenue_cost_over_year:
        years.append(single['year'])
        revenue.append(single['revenue'])
        cost.append(single['cost'])
    context = {
        "business_labels": business_labels,
        "revenue_data": revenue_data,
        "cost_data": cost_data,
        "years": years,
        "revenue": revenue,
        "cost": cost,

    }
    return render(request, 'dashboard.html', context)