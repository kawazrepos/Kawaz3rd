from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from kawaz.core.db.decorators import validate_on_save

class StarManager(models.Manager):
    def get_for_object(self, obj):
        '''Return stars related to the 'obj'.'''
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ct, object_id=obj.pk)

    def add_to_object(self, obj, author, comment='', tag=''):
        '''Add a star to 'obj' and return Star instance.'''
        ct = ContentType.objects.get_for_model(obj)
        star = self.create(author=author, comment=comment, content_type=ct, object_id=obj.pk, tag=tag)
        return star

    def remove_from_object(self, obj, star):
        '''Remove 'star' from 'obj'.'''
        stars = self.get_for_object(obj)
        if not star in stars.all():
            raise AttributeError('The star have not been added to this object.')
        star.delete()

    def cleanup_object(self, obj):
        '''Remove all related stars from 'obj'.'''
        stars = self.get_for_object(obj)
        for star in stars:
            star.delete()

@validate_on_save
class Star(models.Model):
    '''
    Model which indicates stars(like!)
    '''
    content_type = models.ForeignKey(ContentType, verbose_name='Content Type', related_name="content_type_set_for_%(class)s")
    object_id = models.PositiveIntegerField('Object ID')
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    # `comment'はユーザーの引用を格納します。選択した状態で☆を付けると、選択部分がcommentに格納されます。
    comment = models.CharField(_('Comment'), max_length=512, blank=True, default='')
    # 'tag'は☆の種類を表す短い文字列です。例えば将来的にカラースターのような☆に区別を付ける際に利用します
    tag = models.CharField(_('Tag'), max_length=32, blank=True, default='')

    created_at = models.DateTimeField(_('Created at'), auto_now=True)
    objects = StarManager()

    class Meta:
        ordering            = ('created_at',)
        verbose_name        = _('Star')
        verbose_name_plural = _('Stars')
        permissions = (
            ('view_star', 'Can view the Star'),
        )

    def __str__(self):
        return str(self.content_object)

    def clean(self):
        from kawaz.core.permissions.utils import get_full_permission_name
        full_view_perm_name = get_full_permission_name('view', self.content_object)
        if full_view_perm_name in self.content_object._meta.permissions:
            # if model have view permission
            if not self.author.has_perm(full_view_perm_name, obj=self.content_object):
                # 閲覧権限がないオブジェクトにStarをつけようとしたとき、失敗する
                raise PermissionDenied(_("User can't add star to unviewable object"))

from permission import add_permission_logic
from .perms import StarPermissionLogic
add_permission_logic(Star, StarPermissionLogic())
