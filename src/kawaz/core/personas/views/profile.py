from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from permission.decorators.classbase import permission_required
from kawaz.core.views.preview import SingleObjectPreviewViewMixin
from ..forms import ProfileForm
from ..forms import AccountFormSet
from ..models import Profile


@permission_required('personas.change_profile')
class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    formset_prefix = 'accounts'
    template_name = "personas/profile_form.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            'user',
            'skills',
            'accounts__service',
        )
        # WilleはProfile等を持たないため除外
        return qs.exclude(user__role='wille')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated():
            raise Http404(
                _("Anonymous user does not have a profile update view")
            )
        qs = queryset or self.get_queryset()
        return get_object_or_404(qs, user__pk=self.request.user.pk)

    def get_formset(self):
        kwargs = {
            'prefix': 'accounts',
        }
        if self.request.method in ('PUT', 'POST'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({
                'instance': self.object,
            })
        formset = AccountFormSet(**kwargs)
        return formset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.get_formset()
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        # save formset instance. instances require 'profile' attribute thus
        # assign that attribute automatically
        instances = formset.save(commit=False)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        for instance in instances:
            instance._profile = self.request.user._profile
            instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset))

    def get_success_url(self):
        return self.object.user.get_absolute_url()

    def get_success_message(self, cleaned_data):
        return _("Your profile was successfully updated.")


class ProfilePreviewView(SingleObjectPreviewViewMixin, DetailView):
    model = Profile
    template_name = "personas/profile_preview.html"
