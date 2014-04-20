import datetime
from kawaz.core.tests.datetime import patch_datetime_now
from .factories import EventFactory

def static_now():
    """
    Return fixed datetime instance for testing.
    It is mainly for skip Event validation
    """
    return datetime.datetime(2000, 9, 4)

def event_factory_with_relative(b, a, kwargs={}):
    """
    Event factory shortcut function.
    """
    standard_time = static_now()
    kwargs.update(dict(
            period_start=standard_time + datetime.timedelta(days=b),
            period_end=standard_time + datetime.timedelta(days=a),
        ))
    # Event validation system does not allow to make the PAST event thus
    # mock datetime.now to return 1999 for preventing this validation
    _last_year = lambda: static_now() + datetime.timedelta(days=-365)
    with patch_datetime_now(_last_year):
        return EventFactory(**kwargs)