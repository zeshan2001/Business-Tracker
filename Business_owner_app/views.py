from django.shortcuts import render,get_object_or_404
from main_app.models import Business 
from django.views.generic.edit import UpdateView,CreateView,DeleteView
# Create your views here.

class business_Create(CreateView):
    model=Business
    fields="__all__"
    success_url='business/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class business_Updata(UpdateView):
    model=Business
    fields="__all__"
class business_Delete(DeleteView):
    pass

def business(request):
    businesses=Business.objects.all()
    return render(request, 'business.html',{'businesses':businesses})

def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    balance_sheets = business.balance_sheets.all()  
    income_statements = business.income_statements.all()
    context = {
        'business': business,
        'balance_sheets': balance_sheets,
        'income_statements': income_statements,
    }
    return render(request, 'business_detail.html', context)

def profile(request):
    return render(request,'profile.html')