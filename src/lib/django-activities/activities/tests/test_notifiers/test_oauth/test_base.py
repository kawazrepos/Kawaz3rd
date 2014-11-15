# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import tempfile
from contextlib import ExitStack
from unittest.mock import MagicMock, patch
from django.test import TestCase
from ....notifiers.oauth.base import OAuth1ActivityNotifier


TEST_CREDENTIALS = os.path.join(
    os.path.dirname(__file__), 'data', 'credentials.json'
)

class OAuth1ActivityNotifierTestCase(TestCase):
    def setUp(self):
        self.cls = OAuth1ActivityNotifier
        self.cls.request_token_url = MagicMock()
        self.cls.authorization_base_url = MagicMock()
        self.cls.access_token_url = MagicMock()

    def test_attributes(self):
        notifier = self.cls(dict(
            client_key='client_key',
            client_secret='client_secret',
            resource_owner_key='resource_owner_key',
            resource_owner_secret='resource_owner_secret',
        ))
        self.assertTrue(hasattr(notifier, 'url'))
        self.assertTrue(hasattr(notifier, 'key'))
        self.assertTrue(hasattr(notifier, 'params'))
        self.assertTrue(hasattr(notifier, 'request_token_url'))
        self.assertTrue(hasattr(notifier, 'authorization_base_url'))
        self.assertTrue(hasattr(notifier, 'access_token_url'))

        self.assertTrue(callable(getattr(self.cls, 'get_credentials')))
        self.assertTrue(callable(getattr(self.cls, 'create_credentials')))

    def test__init__(self):
        params = {}
        credentials = dict(
            client_key='client_key',
            client_secret='client_secret',
            resource_owner_key='resource_owner_key',
            resource_owner_secret='resource_owner_secret',
        )
        with ExitStack() as stack:
            mOAuth1Session = stack.enter_context(patch(
                'activities.notifiers.oauth.base.OAuth1Session'
            ))
            instance = self.cls(credentials, params)
            mOAuth1Session.assert_called_with(**credentials)
            self.assertEqual(instance.oauth_session,
                             mOAuth1Session.return_value)

    def test_send(self):
        notifier = self.cls(dict(
            client_key='client_key',
            client_secret='client_secret',
            resource_owner_key='resource_owner_key',
            resource_owner_secret='resource_owner_secret',
        ))
        notifier.key = MagicMock()
        notifier.url = MagicMock()
        notifier.oauth_session = MagicMock()
        params = {}
        rendered_content = MagicMock()
        with ExitStack() as stack:
            notifier.send(rendered_content)
            notifier.oauth_session.post.assert_called_with(
                notifier.url,
                data={notifier.key: rendered_content}
            )

    def test_get_credentials(self):
        credentials = self.cls.get_credentials(TEST_CREDENTIALS)
        params = (
            'client_key', 'client_secret',
            'resource_owner_key', 'resource_owner_secret'
        )
        for param in params:
            self.assertEqual(credentials[param], param)

    def test_create_credentials(self):
        import json
        tmpfile = tempfile.mkstemp()[1]
        session = MagicMock()
        with ExitStack() as stack:
            stack.enter_context(patch('builtins.print'))    # to discard output
            minput = stack.enter_context(patch('builtins.input'))
            mdirname = stack.enter_context(patch('os.path.dirname'))
            mOAuth1Session = stack.enter_context(patch(
                'activities.notifiers.oauth.base.OAuth1Session'
            ))
            minput.return_value = '00000000'
            mOAuth1Session.return_value = session

            client_key = 'client_key'
            client_secret = 'client_secret'
            session.fetch_access_token.return_value = dict(
                oauth_token='resource_owner_key',
                oauth_token_secret='resource_owner_secret',
            )

            self.cls.create_credentials(tmpfile, client_key, client_secret)

            mOAuth1Session.assert_called_with(client_key, client_secret)
            session.fetch_request_token.assert_called_with(
                self.cls.request_token_url,
            )
            session.authorization_url.assert_called_with(
                self.cls.authorization_base_url,
            )
            session.fetch_access_token.assert_called_with(
                self.cls.access_token_url, verifier=minput.return_value,
            )

            with open(tmpfile, 'r') as fi:
                credentials = json.load(fi)

                params = (
                    'client_key', 'client_secret',
                    'resource_owner_key', 'resource_owner_secret'
                )
                for param in params:
                    self.assertEqual(credentials[param], param)

        # remove tempfile
        os.remove(tmpfile)
