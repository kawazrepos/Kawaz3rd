from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from kawaz.core.permissions.logics import PUB_STATES

from markupfield.fields import MarkupField

class AnnouncementManager(models.Manager):
    def published(self, user):
        '''
        Returns published announcement for each user
        If `user` is authenticated, it will return public and protected announcements,
        else return public announcements only.
        '''
        q = Q(pub_state='public')
        if user and user.is_authenticated():
            if user.role in ['seele', 'nerv', 'children']:
                # Seele, Nerv, Children can see the protected announcement
                q |= Q(pub_state='protected')
        return self.filter(q)

    def draft(self, user):
        '''
        If `user` is staff user, returns all drafts.
        '''
        if user and user.is_staff:
            return self.filter(pub_state='draft')
        return self.none()
        
class Announcement(models.Model):
    """
    An announcement that came from staff user
    """

    # Required
    pub_state = models.CharField(_('Publish status'), max_length=10, choices=PUB_STATES)
    title = models.CharField(_('Title'), max_length=128)
    body = MarkupField(_('Body'), default_markup_type='markdown')
    silently = models.BooleanField(_('Silently'), default=False,
                                   help_text=_('If you checked this field. This will not be notified anybody.'))
    # Uneditable
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_announcements', editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modified at'), auto_now=True)
    objects = AnnouncementManager()
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        permissions = (
            ('view_announcement', 'Can view the announcement'),
        )

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('announcements_announcement_update', (), {
                'pk' : self.pk
            })
        return ('announcements_announcement_detail', (), {
            'pk' : self.pk
        })

from permission import add_permission_logic
from .perms import AnnouncementPermissionLogic
add_permission_logic(Announcement, AnnouncementPermissionLogic())
