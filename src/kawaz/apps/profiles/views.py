from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from permission.decorators.classbase import permission_required
from .forms import ProfileForm
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


@permission_required('profiles.view_profile')
class ProfileDetailView(DetailView):
    model = Profile
    slug_field = 'user__username'