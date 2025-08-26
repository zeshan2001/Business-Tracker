from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        if profile and profile.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
        return redirect("home")

'''
class Example(RoleRequiredMixin):
    allowed_roles = ["--<role>--"]
'''