# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import datetime
from unittest import mock

_original_datetime_class = datetime.datetime

def patch_datetime_now(mock_now_function):
    """
    Patch datetime.datetime object to apply mock now function.
    It is required because datetime.datetime.now cannot overwrite
    """
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, _original_datetime_class)

    class BaseMockedDatetime(_original_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return mock_now_function()

    # Python2 & Python3 compatible metaclass
    MockedDatetime = DatetimeSubclassMeta('datetime',
                                          (BaseMockedDatetime, ), {})
    return mock.patch('datetime.datetime', MockedDatetime)

