from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from permission.decorators import permission_required
from kawaz.core.views.delete import DeleteSuccessMessageMixin

from .models import Announcement
from .forms import AnnouncementForm


@permission_required('announcements.add_announcement')
class AnnouncementCreateView(SuccessMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return _("""Announcement '%(title)s' successfully created.""") % {
            'title': cleaned_data['title']
        }


@permission_required('announcements.change_announcement')
class AnnouncementUpdateView(SuccessMessageMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm

    def get_success_message(self, cleaned_data):
        return _("""Announcement '%(title)s' successfully updated.""") % {
            'title': cleaned_data['title']
        }


@permission_required('announcements.delete_announcement')
class AnnouncementDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcements_announcement_list')

    def get_success_message(self):
        return _("Announcement successfully deleted.")


@permission_required('announcements.view_announcement')
class AnnouncementDetailView(DetailView):
    model = Announcement


@permission_required('announcements.view_announcement')
class AnnouncementListView(ListView):
    model = Announcement
    paginate_by = 5

    def get_queryset(self):
        return Announcement.objects.published(self.request.user)
