from django.conf import settings
from django.db import models
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
        if user and user.is_authenticated():
            return self.exclude(pub_state='draft')
        return self.filter(pub_state='public')

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_announcements')
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

from permission.logics import PermissionLogic
from permission import add_permission_logic

class AnnouncementPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """

    # announcementは、draftの扱いが異なるため、PubStatePermissionLogicを使用していない
    def _has_view_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'protected':
            # only authorized user can show protected announcement
            return user_obj and user_obj.is_authenticated() and user_obj.role != 'wille'
        if obj.pub_state == 'draft':
            # only staff user can show draft announcement
            return user_obj.is_staff
        # public
        return True

    def has_perm(self, user_obj, perm, obj=None):
        staff_allowed_methods = (
            'announcements.add_announcement',
            'announcements.change_announcement',
            'announcements.delete_announcement',
        )
        if perm in staff_allowed_methods and user_obj.is_staff:
            # all staffs can create / change / delete all announcements
            return True
        if perm == 'announcements.view_announcement' and obj:
            # check view perm by pub_state
            return self._has_view_perm(user_obj, perm, obj)
        return False
add_permission_logic(Announcement, AnnouncementPermissionLogic())
