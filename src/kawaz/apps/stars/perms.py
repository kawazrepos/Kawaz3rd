from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from permission.logics import PermissionLogic
from kawaz.core.permissions.utils import get_full_permission_name

class StarPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """
    def _has_perm_of_content_object(self, user_obj, perm_name, star):
        """
        Check if user have permissions for a content object of `star`
        """
        content_object = star.content_object
        full_perm_name = get_full_permission_name(perm_name, content_object)
        app_label, codename = full_perm_name.split('.')
        ct = ContentType.objects.get_for_model(content_object)
        if Permission.objects.filter(codename=codename, content_type=ct).count() == 0:
            # もし、該当するパーミッションが存在しなければ、常にTrueを返します
            # おもに、perm_nameにviewが渡ってきたときに
            # content_objectのモデルにview権限がそもそも存在しなかった場合は
            # 無条件にTrueが返ります
            # if object don't have `perm_name` return True permanently
            return True
        return user_obj.has_perm(full_perm_name, obj=content_object)

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have a specified star permissions (of obj)
        """
        # filter interest permissions
        if perm not in ('stars.add_star',
                        'stars.change_star',
                        'stars.delete_star',
                        'stars.view_star'):
            return False
        if perm == 'stars.change_star':
            # nobody can change stars
            return False
        if obj is None:
            # seele, nerv, children have following permissions
            permissions = ('stars.add_star',
                           'stars.delete_star',
            )
            roles = ('seele', 'nerv', 'children')
            if perm in permissions and user_obj.is_authenticated() and user_obj.role in roles:
                # seele, nerv, children have permissions of add, change and delete star
                # generally
                return True
            if perm == 'stars.view_star':
                # everybody may be enable to view star.
                return True
            return False
        # object permission
        if perm == 'stars.view_star':
            # users can view a star in following cases.
            # 1 user can view the content_object of star
            # 基本的に全てのスターは誰でも見ることができ、Starそのものには公開状態がないが
            # このチェックをしないと、非公開オブジェクトのStarがpublicなAPIで取れてしまって
            # 引用などが見られてしまう可能性があるので、content_objectが見れる場合のみ閲覧権限がある
            return self._has_perm_of_content_object(user_obj, 'view', obj)
        elif perm == 'stars.delete_star':
            if not user_obj.is_authenticated():
                # anonymous user don't have view perm
                return False
            if user_obj.role not in ('seele', 'nerv', 'children'):
                return False
            # users can delete a star in following cases.
            # 1 user owns the star
            # 2 user can change the content_object of star.
            # このチェックを加えることにより「自分の所持してるオブジェクト」についているStarも削除可能になって嬉しい
            return obj.author == user_obj or self._has_perm_of_content_object(user_obj, 'change', obj)
        return False