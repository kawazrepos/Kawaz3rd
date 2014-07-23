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
from permission.decorators import permission_required
from kawaz.core.views.preview import SingleObjectPreviewMixin
from kawaz.core.personas.models import Persona

from .forms import EntryForm
from .models import Entry


class EntryMultipleObjectMixin(MultipleObjectMixin):
    """
    アクセスしたユーザーにより閲覧可能な記事を指定するためのMixin
    """
    def get_queryset(self):
        return Entry.objects.published(self.request.user)


@permission_required('blogs.view_entry')
class EntryListView(ListView, EntryMultipleObjectMixin):
    model = Entry


@permission_required('blogs.view_entry')
class EntryDetailView(DetailView):
    model = Entry


@permission_required('blogs.add_entry')
class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm

    def get_form(self, form_class):
        # Model.cleanでValidationを行うために
        # ここで作者を設定している
        # 議論参照
        # https://github.com/kawazrepos/Kawaz3rd/pull/134
        form = super().get_form(form_class)
        # 記事の作成者を自動的に指定
        form.instance.author = self.request.user
        return form


@permission_required('blogs.change_entry')
class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm


@permission_required('blogs.delete_entry')
class EntryDeleteView(DeleteView):
    model = Entry


class EntryTodayArchiveView(TodayArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'publish_at'


class EntryDayArchiveView(DayArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'publish_at'
    month_format = '%m'


class EntryMonthArchiveView(MonthArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'publish_at'
    month_format = '%m'


class EntryYearArchiveView(YearArchiveView, EntryMultipleObjectMixin):
    model = Entry
    date_field = 'publish_at'


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
        author = get_object_or_404(Persona, username=username)
        # 著者でQuerySetを更に絞る
        return super().get_queryset().filter(author=author)


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


class EntryPreview(SingleObjectPreviewMixin, DetailView):
    model = Entry
    template_name = "blogs/components/entry_detail.html"
