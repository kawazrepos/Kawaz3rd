from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.forms.formsets import formset_factory

from permission.decorators.classbase import permission_required
from .forms import ProfileForm
from .forms import AccountForm
from .models import Profile

class ProfileListView(ListView):
    model =  Profile

    def get_queryset(self):
        return Profile.objects.published(self.request.user)


@permission_required('profiles.change_profile')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated() and self.request.user:
            return self.request.user.profile
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AccountFormSet = formset_factory(AccountForm, extra=1, can_delete=True)
        context['formset'] = AccountFormSet()
        return context


@permission_required('profiles.view_profile')
class ProfileDetailView(DetailView):
    model = Profile
    slug_field = 'user__username'