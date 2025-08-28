from django.shortcuts import render
from main_app.models import Bank
from main_app.decorators import role_required
from main_app.mixins import RoleRequiredMixin
# Create your views here.
@role_required(allowed_roles=["L"])
def bank(request):
    profile = getattr(request.user, "profile", None)
    bank = Bank.objects.get(id= profile.bank_id)
    
    return render(request, "bank.html", {"bank": bank})