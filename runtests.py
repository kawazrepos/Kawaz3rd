import os, sys
from distutils.version import LooseVersion

def runtests(verbosity=1, interactive=False):
    # Add extra PYTHON_PATH
    root = os.path.abspath(os.path.dirname(__file__))
    required_paths = [
            os.path.join(root, 'src'),
        ]
    for required_path in required_paths:
        if required_path not in sys.path:
            sys.path.insert(0, required_path)
    # django require DJANGO_SETTINGS_MODULE
    os.environ['DJANGO_SETTINGS_MODULE'] = 'kawaz.settings'

    import django
    from django.conf import settings
    from django.test.utils import get_runner
    if LooseVersion(django.get_version()) >= '1.7':
        # django1.7以上の時、setupを呼び出さないと
        # AppRegistryNotReadyを送出する
        # https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
        django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity,
                             interactive=interactive,
                             failfast=False)
    failures = test_runner.run_tests(['kawaz'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
