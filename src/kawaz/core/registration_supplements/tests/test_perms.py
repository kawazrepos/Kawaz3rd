from kawaz.core.tests.testcases.permissions import BasePermissionLogicTestCase

class RegistrationPermissionTestCase(BasePermissionLogicTestCase):
    app_label = 'registration'
    model_name = 'registration_profile'

    def test_accept_registration_model_permission(self):
        """
        accept_registrationのモデルパーミッションをテストします
        seele : True
        nerv : True
        children : False
        wille : False
        anonymous : False
        """
        table = {
            'seele' : True,
            'nerv' : True,
            'children' : False,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='accept_registration', neg=(not pos))

    def test_reject_registration_model_permission(self):
        """
        reject_registrationのモデルパーミッションをテストします
        seele : True
        nerv : True
        children : False
        wille : False
        anonymous : False
        """
        table = {
            'seele' : True,
            'nerv' : True,
            'children' : False,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='reject_registration', neg=(not pos))


    def test_activate_user_model_permission(self):
        """
        activate_userのモデルパーミッションをテストします
        seele : True
        nerv : True
        children : False
        wille : False
        anonymous : False
        """
        table = {
            'seele' : True,
            'nerv' : True,
            'children' : False,
            'wille' : False,
            'anonymous' : False
        }
        for user, pos in table.items():
            self._test(user, perm='activate_user', neg=(not pos))
