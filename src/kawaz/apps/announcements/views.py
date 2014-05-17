from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from permission.decorators import permission_required

from .models import Announcement
from .forms import AnnouncementForm


@permission_required('announcements.add_announcement')
class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@permission_required('announcements.change_announcement')
class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm


@permission_required('announcements.delete_announcement')
class AnnouncementDeleteView(DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcements_announcement_list')


@permission_required('announcements.view_announcement')
class AnnouncementDetailView(DetailView):
    model = Announcement


class AnnouncementListView(ListView):
    model = Announcement

    def get_queryset(self):
        return Announcement.objects.published(self.request.user)
