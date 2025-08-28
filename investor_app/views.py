from django.shortcuts import render
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
from main_app.models import Business


# Create your views here.

@role_required(allowed_roles=["I"])
def investor_dashborad(request):
    businesses = Business.objects.all()
    # profile = getattr(request.user, "profile", None)
    # print(profile.user_id)
    return render(request, "investor_dasborad.html", { 'businesses' : businesses })

@role_required(allowed_roles=["I"])
def investor_detail(request,user_id):
    request.user = user_id
    return render(request, "investor_profile.html")

@role_required(allowed_roles=["I"])
def investment_detail(request):
    return render(request, "investment_detail.html")








# 'investments/', investments_show, name='investor'
# "profile/<int:user_id>", investor_detail, name="investor_profile"