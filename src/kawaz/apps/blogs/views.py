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
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from permission.decorators import permission_required
from kawaz.core.views.preview import SingleObjectPreviewViewMixin
from kawaz.core.personas.models import Persona
from kawaz.core.views.delete import DeleteSuccessMessageMixin

from .forms import EntryForm
from .models import Entry, Category


class EntryMultipleObjectMixin(MultipleObjectMixin):
    """
    アクセスしたユーザーにより閲覧可能な記事を指定するためのMixin
    """
    paginate_by = 5

    def get_queryset(self):
        return Entry.objects.published(self.request.user)


@permission_required('blogs.view_entry')
class EntryListView(ListView, EntryMultipleObjectMixin):
    model = Entry


@permission_required('blogs.view_entry')
class EntryDetailView(DetailView):
    model = Entry


@permission_required('blogs.add_entry')
class EntryCreateView(SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm

    def get_form(self, form_class=EntryForm):
        # Model.cleanでValidationを行うために
        # ここで作者を設定している
        # 議論参照
        # https://github.com/kawazrepos/Kawaz3rd/pull/134
        form = super().get_form(form_class)
        # 記事の作成者を自動的に指定
        form.instance.author = self.request.user
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return _("""A blog entry '%(title)s' was successfully created.""") % {
            'title': cleaned_data['title']
        }


@permission_required('blogs.change_entry')
class EntryUpdateView(SuccessMessageMixin, UpdateView):
    model = Entry
    form_class = EntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return _("""The blog entry '%(title)s' was successfully updated.""") % {
            'title': cleaned_data['title']
        }


@permission_required('blogs.delete_entry')
class EntryDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy('blogs_entry_list')

    def get_success_message(self):
        return _("The blog entry was successfully deleted.")


class EntryTodayArchiveView(TodayArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'published_at'


class EntryDayArchiveView(DayArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'published_at'
    month_format = '%m'


class EntryMonthArchiveView(MonthArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'published_at'
    month_format = '%m'


class EntryYearArchiveView(YearArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'published_at'
    # paginatorを有効にするとき、allow_empty=Trueが必要
    # http://stackoverflow.com/questions/8624507/django-paginate-by-year
    allow_empty = True


class EntryAuthorMixin(EntryMultipleObjectMixin):
    """
    特定ユーザーが執筆した記事に限定して閲覧するためのMixin
    """

    def get_queryset(self):
        # urlにて渡されたユーザーの名前を取得
        # | get('author')だとバグにより urlpattern に author が指定されていない
        # | 場合は None が帰るためバグに気が付きにくい。
        # | したがって敢えて kwargs['author'] と指定している
        username = self.kwargs['author']
        # 名前からインスタンスを指定、存在しない場合は強制404
        self.author = get_object_or_404(Persona, username=username)
        # 著者でQuerySetを更に絞る
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        # ユーザーをコンテキストに入れておく
        data = super().get_context_data(**kwargs)
        data['author'] = self.author
        return data


class EntryAuthorListView(EntryListView, EntryAuthorMixin):
    pass

class EntryAuthorTodayArchiveView(EntryTodayArchiveView, EntryAuthorMixin):
    pass

class EntryAuthorDayArchiveView(EntryDayArchiveView, EntryAuthorMixin):
    pass

class EntryAuthorMonthArchiveView(EntryMonthArchiveView, EntryAuthorMixin):
    pass

class EntryAuthorYearArchiveView(EntryYearArchiveView, EntryAuthorMixin):
    pass


class EntryPreviewView(SingleObjectPreviewViewMixin, DetailView):
    model = Entry
    template_name = "blogs/components/entry_detail.html"


class EntryCategoryListView(EntryAuthorMixin, ListView):
    template_name = 'blogs/entry_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        author = self.kwargs.get('author', None)
        category = self.kwargs.get('pk', None)
        return qs.filter(category__author__username=author, category__pk=int(category))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk', None)
        context['category'] = Category.objects.get(pk=int(category_pk))
        return context
