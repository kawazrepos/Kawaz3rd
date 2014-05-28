import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from markupfield.fields import MarkupField
from kawaz.core.db.decorators import validate_on_save
from kawaz.core.publishments.models import AbstractPublishmentModel
from kawaz.core.publishments.models import PublishmentManagerMixin


class Category(models.Model):
    """
    ブログが所属するカテゴリーモデル

    カテゴリーは各ユーザーがそれぞれ所有するもので、自身のブログの整理に利用する
    目的で存在する。
    """
    label = models.CharField(_('Category name'), max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Author'),
                               related_name='blog_categories',
                               editable=False)

    class Meta:
        # カテゴリはユーザーが所有するものなので unique together を指定
        unique_together = (('author', 'label'),)

    def __str__(self):
        return "{}({})".format(self.label, self.author.username)


class EntryManager(models.Manager, PublishmentManagerMixin):
    pass


@validate_on_save
class Entry(AbstractPublishmentModel):
    """
    ブログ記事モデル
    """
    title = models.CharField(_('Title'), max_length=255)
    body = MarkupField(_('Body'), default_markup_type='markdown')
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 related_name="entries",
                                 blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Author'),
                               related_name='blog_entries', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    publish_at = models.DateTimeField(_('Published at'),
                                      null=True, editable=False)

    objects = EntryManager()

    class Meta:
        ordering = ('-updated_at', 'title')
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        permissions = (
            ('view_entry', 'Can view the entry'),
        )

    def __str__(self):
        return self.title

    @property
    def publish_at_date(self):
        """公開日"""
        if not self.publish_at:
            return None
        return datetime.datetime.date(self.publish_at)

    def save(self, *args, **kwargs):
        if not self.publish_at:
            # 記事の状態が下書き以外の場合は公開日時を自動的に指定
            # これは最初の公開時のみに行われるため 公開->下書き->公開 としても
            # 最初の公開日が変更されることはない
            if self.pub_state != 'draft':
                self.publish_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.category and self.author != self.category.author:
            raise ValidationError('Category must be owned by author.')
        super().clean()

    @models.permalink
    def get_absolute_url(self):
        if self.publish_at:
            return ('blogs_entry_detail', (), {
                'author': self.author.username,
                'year': self.publish_at.year,
                'month': self.publish_at.month,
                'day': self.publish_at.day,
                'pk': self.pk
            })
        return ('blogs_entry_update', (), {
            'author': self.author.username,
            'pk': self.pk
        })


from permission import add_permission_logic
from permission.logics.author import AuthorPermissionLogic
from kawaz.core.publishments.perms import PublishmentPermissionLogic

add_permission_logic(Entry, AuthorPermissionLogic(
    field_name='author',
    any_permission=True,
))
add_permission_logic(Entry, PublishmentPermissionLogic())
