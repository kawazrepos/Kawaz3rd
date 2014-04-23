from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TodayArchiveView
from django.views.generic import DayArchiveView
from django.views.generic import MonthArchiveView
from django.views.generic import YearArchiveView
from django.views.generic.dates import MultipleObjectMixin

from django.shortcuts import get_object_or_404

from kawaz.core.personas.models import Persona

from .models import Entry

class EntryListView(ListView):
    '''
    View class for listing all entries
    '''
    model = Entry


class EntryDetailView(DetailView):
    '''
    View class for details of blog entries.
    '''
    model = Entry


class EntryCreateView(CreateView):
    '''
    View class for blog entry creation
    '''
    model = Entry


class EntryUpdateView(UpdateView):
    '''
    View class for updating blog entries
    '''
    model = Entry


class EntryDeleteView(DeleteView):
    '''
    View class for deleting blog entries.
    '''
    model = Entry


class EntryTodayArchiveView(TodayArchiveView):
    '''
    View class for listing blog entries written on today.
    '''
    model = Entry


class EntryDayArchiveView(DayArchiveView):
    '''
    View class for listing blog entries written in the day.
    '''
    model = Entry


class EntryMonthArchiveView(MonthArchiveView):
    '''
    View class for listing blog entries written in the month
    '''
    model = Entry


class EntryYearArchiveView(YearArchiveView):
    '''
    View class for listing blog entries written in the year.
    '''
    model = Entry


class EntryAuthorMixin(MultipleObjectMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs.get('author')
        author = get_object_or_404(Persona, username=username)
        return qs.filter(author=author)


class EntryAuthorListView(EntryListView, EntryAuthorMixin):
    '''
    View class for listing for all entries of specific author.
    '''

class EntryAuthorTodayArchiveView(EntryTodayArchiveView, EntryAuthorMixin):
    '''
    View class for listing for entries written on today of specific author.
    '''


class EntryAuthorDayArchiveView(EntryDayArchiveView, EntryAuthorMixin):
    '''
    View class for listing for entries written in the day of specific author.
    '''


class EntryAuthorMonthArchiveView(EntryMonthArchiveView, EntryAuthorMixin):
    '''
    View class for listing for entries written in the month of specific author.
    '''

class EntryAuthorYearArchiveView(EntryYearArchiveView, EntryAuthorMixin):
    '''
    View class for listing for entries written in the year of specific author.
    '''
