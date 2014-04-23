import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from markupfield.fields import MarkupField

from kawaz.core.db.decorators import validate_on_save
from kawaz.core.permissions.logics import PUB_STATES

User = get_user_model()

class Category(models.Model):
    '''The model which indicates category of each entries'''
    label = models.CharField(_('Category name'), max_length=255)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='blog_categories', editable=False)
    
    class Meta:
        unique_together = (('author', 'label'),) 
    
    def __str__(self):
        return '%s(%s)' % (self.label, self.author.username)


class EntryManager(models.Manager):
    '''The model manager for Entry'''

    def published(self, user):
        '''Returns Queryset which contains viewable objects by ``user``.'''
        q = Q(pub_state='public')
        if user and user.is_authenticated():
            if not user.role in 'wille':
                q |= Q(pub_state='protected')
        return self.filter(q).distinct()

    def draft(self, user):
        '''Returns Queryset contains draft entries which owned by ``user``.'''
        if user and user.is_authenticated():
            return self.filter(author=user, pub_state='draft')
        return self.none()


@validate_on_save
class Entry(models.Model):
    '''Entry model of blog'''
    pub_state = models.CharField(_('Publish status'), max_length=10, choices=PUB_STATES, default="public")
    title = models.CharField(_('Title'), max_length=255)
    
    body = MarkupField(_('Body'), default_markup_type='markdown')
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name="entries", blank=True, null=True)
    
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='blog_entries', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    publish_at = models.DateTimeField(_('Published at'), null=True, editable=False)

    objects = EntryManager()

    class Meta:
        ordering = ('-updated_at', 'title')
        unique_together = (('title', 'author',),)
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        permissions = (
            ('view_entry', 'Can view the entry'),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.publish_at:
            if self.pub_state == 'draft':
                # if drafted and haven't published yet set publish_at = None
                self.publish_at = None
            else:
                self.publish_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.category and self.author != self.category.author:
            raise ValidationError('Category must be owned by author.')
        super().clean()

    @property
    def publish_at_date(self):
        '''return Publish date'''
        return datetime.datetime.date(self.publish_at)

from permission import add_permission_logic
from permission.logics.author import AuthorPermissionLogic
from kawaz.core.permissions.logics import PubStatePermissionLogic

add_permission_logic(Entry, AuthorPermissionLogic(
    field_name='author',
    any_permission=True,
))
add_permission_logic(Entry, PubStatePermissionLogic())
