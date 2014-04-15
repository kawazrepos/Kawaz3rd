import os, sys

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

    from django.conf import settings
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity,
                             interactive=interactive,
                             failfast=False)
    failures = test_runner.run_tests(['kawaz'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
