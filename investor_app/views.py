from django.shortcuts import render
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
from main_app.models import Business


# Create your views here.

@role_required(allowed_roles=["I"])
def investor_dashborad(request):
    businesses = Business.objects.all()
    return render(request, "investor_dasborad.html", { 'businesses' : businesses })

@role_required(allowed_roles=["I"])
def investor_detail(request,user_id):
    request.user = user_id
    return render(request, "investor_profile.html")

@role_required(allowed_roles=["I"])
def investment_detail(request, business_id):
    business_id = Business.objects.get(id=business_id,)
    # business = Business.objects.get(id=business_id)
    return render(request, "investment_detail.html", { 'business_id' : business_id })
