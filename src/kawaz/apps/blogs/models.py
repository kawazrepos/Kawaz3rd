import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from markupfield.fields import MarkupField

from kawaz.core.db.decorators import validate_on_save
from kawaz.core.permissions.logics import PUB_STATES


class Category(models.Model):
    '''The model which indicates category of each entries'''
    label = models.CharField(_('Category name'), max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), related_name='blog_categories', editable=False)
    
    class Meta:
        unique_together = (('author', 'label'),) 
    
    def __str__(self):
        return '%s(%s)' % (self.label, self.author.username)

@validate_on_save
class Entry(models.Model):
    '''Entry model of blog'''
    pub_state = models.CharField(_('Publish status'), max_length=10, choices=PUB_STATES, default="public")
    title = models.CharField(_('Title'), max_length=255)
    
    body = MarkupField(_('Body'), default_markup_type='markdown')
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name="entries", blank=True, null=True)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), related_name='blog_entries', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    publish_at = models.DateTimeField(_('Published at'), null=True, editable=False)

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
        if self.pk == None:
            if self.pub_state == 'draft':
                self.publish_at = None
            elif self.publish_at == None:
                self.publish_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.category and self.author != self.category.author:
            raise ValidationError('Category must be owned by author.')
        super().clean()

from permission import add_permission_logic
from permission.logics.author import AuthorPermissionLogic
from kawaz.core.permissions.logics import PubStatePermissionLogic

add_permission_logic(Entry, AuthorPermissionLogic(
    field_name='author',
    any_permission=True,
))
add_permission_logic(Entry, PubStatePermissionLogic())
