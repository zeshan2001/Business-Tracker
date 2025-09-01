from django.shortcuts import render,get_object_or_404, redirect
from main_app.decorators import role_required
from main_app.models import Business, Profile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views import View

from main_app.mixins import RoleRequiredMixin
from main_app.forms import ProfileForm
from django.contrib.auth.models import User

# Create your views here.

@role_required(allowed_roles=["I"])
def investor_dashborad(request):
    businesses = Business.objects.all()
    return render(request, "investor_dasborad.html", { 'businesses' : businesses })

# @role_required(allowed_roles=["I"])
# def investor_detail(request,user_id):
#     request.user = user_id
#     return render(request, "investor_profile.html")


class ProfileDetail(View):

    def get(self, request):
        owner = Profile.objects.get(user=request.user)
        return render(request, 'Investor_Profile.html', {'owner': owner})

class ProfileUpdate(UpdateView):
    model = Profile
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


class ProfileDelete(View):
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

    return render(request, "investment_detail.html", { 'business_id' : business_id, 'owner': owner })
