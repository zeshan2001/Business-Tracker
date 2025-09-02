from django.shortcuts import redirect

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login") 
            profile = getattr(request.user, "profile", None)
            if profile and profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect("home") 
        return wrapper
    return decorator

'''
how to use it 
@role_required(allowed_roles["--<role>--"])
def name():
'''