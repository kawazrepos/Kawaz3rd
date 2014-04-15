import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from markupfield.fields import MarkupField

class Category(models.Model):
    '''The model which indicates category of each entries'''
    label = models.CharField(_('Category name'), max_length=255)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='blog_categories', editable=False)
    
    class Meta:
        unique_together = (('author', 'label'),) 
    
    def __str__(self):
        return self.label

class Entry(models.Model):
    '''Entry model of blog'''
    PUB_STATES = (
        ('public',      _("Public")),
        ('protected',   _("Internal")),
        ('draft',       _("Draft")),
    )

    pub_state = models.CharField(_('Publish status'), max_length=10, choices=PUB_STATES, default="public")
    title = models.CharField(_('Title'), max_length=255)
    
    body = MarkupField(_('Body'), default_markup_type='markdown')
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name="entries", blank=True, null=True)
    
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='blog_entries', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    publish_at = models.DateTimeField(_('Published at'), null=True, editable=False)

    class Meta:
        ordering = ('-updated_at', 'title')
        unique_together = (('title', 'author',),)
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pub_state == 'draft':
            self.publish_at = None
        else:
            self.publish_at = datetime.datetime.now()
        super(Entry, self).save(*args, **kwargs)
