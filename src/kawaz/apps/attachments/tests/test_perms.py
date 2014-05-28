from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase

class RegistrationPermissionTestCase(BasePermissionLogicTestCase):
    app_label = 'attachments'
    model_name = 'material'

    def test_add_attachment_model_permission(self):
        """
        add_attachmentのモデルパーミッションをテストします
        seele : True
        nerv : True
        children : True
        wille : False
        anonymous : False
        """
        table = {
            'seele' : True,
            'nerv' : True,
            'children' : True,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='add', neg=(not pos))

    def test_change_attachment_model_permission(self):
        """
        change_attachmentのモデルパーミッションをテストします
        seele : False
        nerv : False
        children : False
        wille : False
        anonymous : False
        """
        table = {
            'seele' : False,
            'nerv' : False,
            'children' : False,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='change', neg=(not pos))

    def test_delete_attachment_model_permission(self):
        """
        delete_attachmentのモデルパーミッションをテストします
        seele : False
        nerv : False
        children : False
        wille : False
        anonymous : False
        """
        table = {
            'seele' : False,
            'nerv' : False,
            'children' : False,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='delete', neg=(not pos))
