from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from permission.decorators.classbase import permission_required
from .forms import ProfileForm
from .forms import AccountForm
from .models import Profile
from .forms import get_account_formset

class ProfileListView(ListView):
    model =  Profile

    def get_queryset(self):
        return Profile.objects.published(self.request.user)


@permission_required('profiles.change_profile')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    formset_prefix = 'accounts'

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated() and self.request.user:
            return self.request.user.profile
        return None

    def post(self, request, *args, **kwargs):
        # formsetの中身も保存するために複雑なことをしている
        # ToDo 実装上の問題を抱えているから後で直す
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        AccountFormSet = get_account_formset()
        formset = AccountFormSet(request.POST, request.FILES, prefix=self.formset_prefix)
        if form.is_valid() and formset.is_valid():
            instances = formset.save(commit=False)
            for account in instances:
                account.user = request.user
                account.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Account formsetを作成して渡す
        AccountFormSet = get_account_formset()
        context['formset'] = AccountFormSet(prefix=self.formset_prefix)
        return context


@permission_required('profiles.view_profile')
class ProfileDetailView(DetailView):
    model = Profile
    slug_field = 'user__username'