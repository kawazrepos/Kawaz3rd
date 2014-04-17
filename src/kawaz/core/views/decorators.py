from django.utils.decorators import method_decorator

def class_view_decorator(function_decorator):
    """
    Convert a function based decorator into a class based decorator usable on class based Views.
        >>> from django.contrib.auth.models import User
        >>> from django.views.generic.detail import DetailView
        >>> from django.contrib.auth.decorators import login_required
        >>> @class_view_decorator(login_required)
        >>> class UserDetailView(DetailView):
        >>>     model = User
    """

    def _wrapper(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return _wrapper