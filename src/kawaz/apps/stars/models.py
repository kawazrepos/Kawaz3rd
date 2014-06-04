from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from kawaz.core.db.decorators import validate_on_save


class StarManager(models.Manager):
    def get_for_object(self, obj):
        """
        指定されたオブジェクトに関係するスターを含むクエリを返す

        Args:
            obj (model instance): 検索対象のモデルインスタンス
        """
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ct, object_id=obj.pk)

    def add_to_object(self, obj, author, quote=''):
        """
        指定されたオブジェクトに新たにスターを作成

        Args:
            obj (model instance): 付加対象のモデルインスタンス
            author (user instance): スター付加を行うユーザー
            quote (str): 引用文字列（デフォルト: `''`）

        Notice:
            `author`を指定するが、実際に`author`がstarを対象オブジェクトに
            付加可能かどうかのテストは行わない。
            このテストを行う場合は下記のように権限テストを行う必要がある

            >>> author.has_perm('stars.add_star', obj=obj)

        """
        ct = ContentType.objects.get_for_model(obj)
        star = self.create(content_type=ct,
                           object_id=obj.pk,
                           author=author,
                           quote=quote)
        return star

    def remove_from_object(self, obj, star):
        """
        指定されたオブジェクトから指定されたスターを削除

        Args:
            obj (model instance): 削除対象のモデルインスタンス
            star (star instance): 削除対象のスターインスタンス

        Raises:
            ObjectDoesNotExist: 指定されたスターがオブジェクトに関連付けられて
                居ない場合に発生
        """
        stars = self.get_for_object(obj)
        if star not in stars.all():
            raise ObjectDoesNotExist(
                _('The star have not been added to this object.'))
        star.delete()

    def cleanup_object(self, obj):
        """
        指定されたオブジェクトに付加されている全てのスターを削除

        Args:
            obj (model instance): 削除対象のモデルインスタンス
        """
        stars = self.get_for_object(obj)
        for star in stars:
            star.delete()


@validate_on_save
class Star(models.Model):
    """
    はてなスター的なモデル。主にJavaScriptで処理を行う
    """
    content_type = models.ForeignKey(
        ContentType,
        verbose_name='Content Type',
        related_name="content_type_set_for_%(class)s")
    object_id = models.PositiveIntegerField('Object ID')
    content_object = GenericForeignKey(ct_field="content_type",
                                       fk_field="object_id")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Author'))
    # ユーザーが記事の一部分を選択した状態でスターを押した場合、その部分を
    # 引用として格納する
    quote = models.CharField(_('Quote'),
                             max_length=512, blank=True, default='',
                             help_text=_("This is used for quotation. "
                                         "When the user add a star with text "
                                         "selection, the selected text is "
                                         "passed to this."))
    created_at = models.DateTimeField(_('Created at'), auto_now=True)

    objects = StarManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')
        permissions = (
            ('view_star', 'Can view the Star'),
        )

    def __str__(self):
        return str(self.content_object)


from permission import add_permission_logic
from .perms import StarPermissionLogic
add_permission_logic(Star, StarPermissionLogic())
