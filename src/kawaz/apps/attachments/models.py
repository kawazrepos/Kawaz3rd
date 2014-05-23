import os
from django.db import models
from django.utils.translation import ugettext as _
from kawaz.core.personas.models import Persona

class Material(models.Model):
    """
    添付素材用のモデルです
    """
    def _get_upload_path(self, filename):
        basedir = os.path.join('materials', self.author.username)
        return os.path.join(basedir, filename)

    content_file = models.FileField(_('Content file'), upload_to=_get_upload_path)
    author = models.ForeignKey(Persona, verbose_name=_('Author'), editable=False)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)
    ip_address  = models.IPAddressField("IP Address", editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        ordering = _('created_at',)
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')

    @property
    def ext(self):
        """
        アップされたファイルから拡張子を返します
        拡張子は小文字になります。2つ以上拡張子がついている場合は最後の物のみが返却されます。
            hoge.mp3 -> mp3
            hoge.tar.gz -> gz
            hoge.WAV -> wav
        """
        ext = os.path.splitext(self.content_file.name)[1]
        if ext:
            return ext[1:].lower()
        return ''

    @property
    def is_image (self):
        """
        画像ファイルかどうかを返します
        """
        extensions = ['jpg', 'jpeg', 'png', 'gif']
        return self.ext in extensions

    @property
    def is_audio(self):
        """
        音声ファイルかどうかを返します
        """
        extensions = ['wav', 'mp3']
        return self.ext in extensions

    @property
    def is_movie(self):
        """
        動画ファイルかどうかを返します
        """
        extensions = ['mov', 'mp4']
        return self.ext in extensions

from permission import add_permission_logic
from permission.logics import AuthorPermissionLogic
from kawaz.core.permissions.logics import ChildrenPermissionLogic
add_permission_logic(Material, AuthorPermissionLogic(
    field_name='author',
    change_permission=True,
    delete_permission=True
))
add_permission_logic(Material, ChildrenPermissionLogic(
    add_permission=True,
    change_permission=False,
    delete_permission=False
))